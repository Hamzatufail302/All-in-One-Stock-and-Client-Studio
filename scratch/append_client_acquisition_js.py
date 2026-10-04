# Append client acquisition logic to static/js/app.js
import os

js_code = r'''
// =========================================================================
// VIDEO CLIENT ACQUISITION & OUTREACH ENGINE
// =========================================================================

async function loadClientAcquisitionTab() {
    const container = document.getElementById('tab-client-acquisition');
    if (!container) return;

    if (!state.clientAcquisition || !state.clientAcquisition.overview) {
        container.innerHTML = `
            <div class="glass-panel p-12 rounded-3xl text-center border border-slate-800">
                <div class="inline-block p-4 rounded-2xl bg-pink-500/10 text-pink-400 mb-4 animate-pulse">
                    <i data-lucide="video" class="w-8 h-8"></i>
                </div>
                <h3 class="text-lg font-bold text-white mb-2">Loading Video Client Acquisition Engine...</h3>
                <p class="text-xs text-slate-400">Fetching 2026 pacing specs, client playbooks, cold scripts, and CRM pipeline</p>
            </div>
        `;
        if (window.lucide) lucide.createIcons();
    }

    try {
        const [overviewRes, leadsRes] = await Promise.all([
            fetch('/api/client-acquisition/overview'),
            fetch('/api/client-acquisition/leads')
        ]);
        if (overviewRes.ok) {
            state.clientAcquisition.overview = await overviewRes.json();
        }
        if (leadsRes.ok) {
            const leadsData = await leadsRes.json();
            state.clientAcquisition.leads = leadsData.leads || [];
        }
    } catch (err) {
        console.error('Error fetching client acquisition data:', err);
        showToast('Failed to load client acquisition data', 'error');
    }

    renderClientAcquisitionUI();
}

function switchAcquisitionSubTab(tabKey) {
    if (!state.clientAcquisition) state.clientAcquisition = {};
    state.clientAcquisition.activeSubTab = tabKey;
    renderClientAcquisitionUI();
}

function prefillPitchGenerator(nicheTitle, styleCategory) {
    if (!state.clientAcquisition) state.clientAcquisition = {};
    state.clientAcquisition.activeSubTab = 'generator';
    state.clientAcquisition.prefilledNiche = `${nicheTitle} (${styleCategory})`;
    renderClientAcquisitionUI();
    showToast(`Pre-filled pitch generator for ${nicheTitle}!`, 'info');
}

async function handleGeneratePitch() {
    const nameInput = document.getElementById('pitch-client-name');
    const nicheInput = document.getElementById('pitch-client-niche');
    const typeInput = document.getElementById('pitch-type-select');
    const linkInput = document.getElementById('pitch-custom-link');

    const clientName = nameInput ? nameInput.value.trim() : '';
    const channelNiche = nicheInput ? nicheInput.value.trim() : '';
    const pitchType = typeInput ? typeInput.value : 'youtube_sample';
    const customLink = linkInput ? linkInput.value.trim() : '';

    if (!clientName || !channelNiche) {
        showToast('Please enter both Creator/Client Name and Niche/Channel', 'info');
        return;
    }

    try {
        const res = await fetch('/api/client-acquisition/generate-pitch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                client_name: clientName,
                channel_or_niche: channelNiche,
                pitch_type: pitchType,
                custom_link: customLink
            })
        });
        if (!res.ok) throw new Error('Generation failed');
        const data = await res.json();
        state.clientAcquisition.generatedPitch = data;
        state.clientAcquisition.lastPitchInputs = { clientName, channelNiche, pitchType, customLink };
        renderClientAcquisitionUI();
        showToast('High-converting pitch generated successfully!', 'success');
    } catch (e) {
        console.error(e);
        showToast('Failed to generate pitch. Please try again.', 'error');
    }
}

async function saveCurrentPitchAsLead() {
    const p = state.clientAcquisition.generatedPitch;
    const inp = state.clientAcquisition.lastPitchInputs || {};
    if (!p) {
        showToast('Generate a pitch first before saving as lead', 'info');
        return;
    }

    const payload = {
        client_name: p.client_name || inp.clientName || 'Target Client',
        channel_or_website: inp.customLink || '',
        client_niche: p.niche || inp.channelNiche || 'YouTube',
        outreach_channel: inp.pitchType === 'short_dm' ? 'Instagram/Twitter DM' : (inp.pitchType === 'upwork' ? 'Upwork' : 'Email'),
        pitch_content: `Subject: ${p.subject}\n\n${p.body}`,
        status: 'Targeted',
        followup_date: new Date(Date.now() + 4 * 86400000).toISOString().split('T')[0],
        notes: `Generated via AI Pitch Engine (${inp.pitchType || 'custom'})`
    };

    try {
        const res = await fetch('/api/client-acquisition/leads', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            showToast('Lead saved into Outreach CRM pipeline!', 'success');
            const leadsRes = await fetch('/api/client-acquisition/leads');
            if (leadsRes.ok) {
                const ld = await leadsRes.json();
                state.clientAcquisition.leads = ld.leads || [];
            }
            state.clientAcquisition.activeSubTab = 'crm';
            renderClientAcquisitionUI();
        }
    } catch (err) {
        console.error(err);
        showToast('Failed to save lead to CRM', 'error');
    }
}

async function handleAddNewLead() {
    const name = (document.getElementById('new-lead-name')?.value || '').trim();
    const channel = (document.getElementById('new-lead-channel')?.value || '').trim();
    const niche = (document.getElementById('new-lead-niche')?.value || 'YouTube').trim();
    const outreachCh = document.getElementById('new-lead-outreach-channel')?.value || 'Email';
    const status = document.getElementById('new-lead-status')?.value || 'Targeted';
    const followup = document.getElementById('new-lead-followup')?.value || '';
    const notes = (document.getElementById('new-lead-notes')?.value || '').trim();

    if (!name) {
        showToast('Please enter the client / creator name', 'info');
        return;
    }

    const payload = {
        client_name: name,
        channel_or_website: channel,
        client_niche: niche,
        outreach_channel: outreachCh,
        pitch_content: '',
        status: status,
        followup_date: followup,
        notes: notes
    };

    try {
        const res = await fetch('/api/client-acquisition/leads', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            showToast('New client lead added to CRM!', 'success');
            const leadsRes = await fetch('/api/client-acquisition/leads');
            if (leadsRes.ok) {
                const ld = await leadsRes.json();
                state.clientAcquisition.leads = ld.leads || [];
            }
            renderClientAcquisitionUI();
        }
    } catch (err) {
        console.error(err);
        showToast('Failed to add lead', 'error');
    }
}

async function updateLeadStatus(leadId, newStatus) {
    try {
        const res = await fetch(`/api/client-acquisition/leads/${leadId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        });
        if (res.ok) {
            showToast(`Status updated to ${newStatus}`, 'success');
            const target = state.clientAcquisition.leads.find(l => l.id === leadId);
            if (target) target.status = newStatus;
            renderClientAcquisitionUI();
        }
    } catch (err) {
        console.error(err);
        showToast('Failed to update status', 'error');
    }
}

async function deleteLead(leadId) {
    if (!confirm('Are you sure you want to remove this lead from your outreach CRM?')) return;
    try {
        const res = await fetch(`/api/client-acquisition/leads/${leadId}`, {
            method: 'DELETE'
        });
        if (res.ok) {
            showToast('Lead deleted from pipeline', 'info');
            state.clientAcquisition.leads = state.clientAcquisition.leads.filter(l => l.id !== leadId);
            renderClientAcquisitionUI();
        }
    } catch (err) {
        console.error(err);
        showToast('Failed to delete lead', 'error');
    }
}

function renderClientAcquisitionUI() {
    const container = document.getElementById('tab-client-acquisition');
    if (!container) return;

    const ov = state.clientAcquisition.overview || {};
    const reqs = ov.current_requirements || [];
    const playbooks = ov.prospecting_playbooks || [];
    const templates = ov.cold_email_templates || [];
    const objections = ov.objection_handling || [];
    const presets = ov.retainer_presets || [];
    const leads = state.clientAcquisition.leads || [];
    const activeSubTab = state.clientAcquisition.activeSubTab || 'requirements';

    // Count metrics
    const totalLeads = leads.length;
    const samplesSent = leads.filter(l => l.status === 'Sample Sent').length;
    const callsBooked = leads.filter(l => l.status === 'Call Booked').length;
    const closedRetainers = leads.filter(l => l.status === 'Closed Retainer').length;

    // Sub-tab definitions
    const subTabs = [
        { id: 'requirements', label: 'Video Specs & Demands', icon: 'film', badge: reqs.length },
        { id: 'playbooks', label: 'Client Playbooks & Search Queries', icon: 'crosshair', badge: playbooks.length },
        { id: 'generator', label: 'AI Custom Pitch Generator', icon: 'sparkles', badge: 'Live' },
        { id: 'templates', label: 'Cold Emails & Objections', icon: 'mail', badge: templates.length + objections.length },
        { id: 'calculator', label: 'Retainer & Income Roadmaps', icon: 'dollar-sign', badge: '3 Tiers' },
        { id: 'crm', label: 'Client Outreach CRM', icon: 'users', badge: totalLeads }
    ];

    let html = `
        <!-- Hero Header -->
        <div class="relative rounded-3xl p-8 sm:p-10 overflow-hidden glass-panel border border-pink-500/25 shadow-2xl">
            <div class="absolute -right-20 -top-20 w-96 h-96 bg-pink-600/15 rounded-full blur-3xl pointer-events-none"></div>
            <div class="absolute -left-20 -bottom-20 w-96 h-96 bg-purple-600/15 rounded-full blur-3xl pointer-events-none"></div>

            <div class="relative z-10 max-w-4xl">
                <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-pink-500/15 border border-pink-500/30 text-pink-300 text-xs font-semibold mb-3.5 shadow-sm">
                    <i data-lucide="video" class="w-3.5 h-3.5"></i>
                    Video Editor Client Acquisition & High-Ticket Outreach Engine
                </div>
                <h1 class="text-3xl sm:text-4xl font-black text-white tracking-tight leading-tight">
                    How to Find, Pitch & Close <span class="bg-gradient-to-r from-pink-400 via-purple-300 to-indigo-400 bg-clip-text text-transparent">High-Ticket Video Editing Clients</span>
                </h1>
                <p class="mt-2 text-slate-300 text-sm leading-relaxed max-w-3xl">
                    Stop applying to crowded gig posts. Master 2026 retention demands, use targeted search operators to find active creators & founders, send custom hook samples with zero friction, and manage monthly retainers.
                </p>

                <!-- Top Quick Metrics -->
                <div class="mt-6 grid grid-cols-2 sm:grid-cols-4 gap-3">
                    <div class="p-3.5 rounded-2xl bg-slate-900/80 border border-slate-800 backdrop-blur-md">
                        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Top Video Niches</div>
                        <div class="text-xl font-black text-white mt-0.5">${reqs.length} High-Ticket Styles</div>
                        <div class="text-[10px] text-pink-400 font-mono mt-0.5">$200–$3,000/project</div>
                    </div>
                    <div class="p-3.5 rounded-2xl bg-slate-900/80 border border-slate-800 backdrop-blur-md">
                        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Acquisition Channels</div>
                        <div class="text-xl font-black text-white mt-0.5">${playbooks.length} Active Playbooks</div>
                        <div class="text-[10px] text-indigo-400 font-mono mt-0.5">YouTube, X, LinkedIn, Maps</div>
                    </div>
                    <div class="p-3.5 rounded-2xl bg-slate-900/80 border border-slate-800 backdrop-blur-md">
                        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Active CRM Pipeline</div>
                        <div class="text-xl font-black text-white mt-0.5">${totalLeads} Tracked Leads</div>
                        <div class="text-[10px] text-emerald-400 font-mono mt-0.5">${closedRetainers} Closed Retainers</div>
                    </div>
                    <div class="p-3.5 rounded-2xl bg-slate-900/80 border border-slate-800 backdrop-blur-md">
                        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Response Benchmark</div>
                        <div class="text-xl font-black text-white mt-0.5">25% – 35% Reply Rate</div>
                        <div class="text-[10px] text-amber-400 font-mono mt-0.5">With Re-Edited Hook Sample</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Sub-Navigation Navigation Pills -->
        <div class="flex items-center gap-2 overflow-x-auto no-scrollbar pb-1">
            ${subTabs.map(st => {
                const isActive = activeSubTab === st.id;
                return `
                    <button onclick="switchAcquisitionSubTab('${st.id}')" class="px-4 py-2.5 rounded-2xl text-xs font-bold flex items-center gap-2 whitespace-nowrap transition shadow-sm ${
                        isActive
                            ? 'bg-gradient-to-r from-pink-600 to-purple-600 text-white shadow-pink-600/25 border border-pink-500/40'
                            : 'bg-slate-900/80 text-slate-300 hover:text-white hover:bg-slate-800 border border-slate-800'
                    }">
                        <i data-lucide="${st.icon}" class="w-3.5 h-3.5 ${isActive ? 'text-white' : 'text-pink-400'}"></i>
                        <span>${st.label}</span>
                        <span class="px-1.5 py-0.2 rounded-full text-[10px] font-mono ${isActive ? 'bg-black/30 text-white' : 'bg-slate-800 text-slate-400'}">${st.badge}</span>
                    </button>
                `;
            }).join('')}
        </div>
    `;

    // SUB-TAB 1: REQUIREMENTS & PACING SPECS
    if (activeSubTab === 'requirements') {
        html += `
            <div class="space-y-6">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div>
                        <h2 class="text-2xl font-black text-white tracking-tight">2026 High-Ticket Video Client Requirements & Demands</h2>
                        <p class="text-xs text-slate-400 mt-1">What paying creators, founders, and agencies are actively hiring for right now</p>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    ${reqs.map(r => `
                        <div class="glass-panel rounded-3xl p-6 border border-slate-800/90 shadow-xl flex flex-col justify-between hover:border-pink-500/40 transition">
                            <div class="space-y-4">
                                <div class="flex items-start justify-between gap-3">
                                    <div class="flex items-center gap-3">
                                        <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-pink-500/20 to-purple-500/20 border border-pink-500/30 flex items-center justify-center text-pink-400">
                                            <i data-lucide="${r.icon || 'video'}" class="w-5 h-5"></i>
                                        </div>
                                        <div>
                                            <h3 class="text-lg font-black text-white">${escapeHtml(r.title)}</h3>
                                            <span class="text-xs font-semibold text-slate-400">${escapeHtml(r.style_category)}</span>
                                        </div>
                                    </div>
                                    <span class="px-2.5 py-1 rounded-xl text-[10px] font-black bg-pink-500/10 text-pink-300 border border-pink-500/30 font-mono shrink-0">${escapeHtml(r.market_demand)}</span>
                                </div>

                                <!-- Pricing & Target -->
                                <div class="p-3.5 rounded-2xl bg-slate-900/90 border border-slate-800/80 space-y-1.5">
                                    <div class="flex items-center justify-between text-xs">
                                        <span class="text-slate-400 font-medium">Average Market Rates:</span>
                                        <span class="font-bold text-emerald-400 font-mono">${escapeHtml(r.avg_pricing)}</span>
                                    </div>
                                    <div class="text-[11px] text-slate-300">
                                        <strong class="text-white">Ideal Clients:</strong> ${escapeHtml(r.ideal_clients)}
                                    </div>
                                </div>

                                <!-- Pacing & Deliverables -->
                                <div class="space-y-2 text-xs">
                                    <div class="p-3 rounded-2xl bg-slate-950/60 border border-slate-800">
                                        <div class="text-[11px] font-bold text-amber-400 flex items-center gap-1.5 mb-1">
                                            <i data-lucide="zap" class="w-3.5 h-3.5"></i>
                                            <span>Retention & Pacing Rules:</span>
                                        </div>
                                        <p class="text-slate-300 text-[11px] leading-relaxed">${escapeHtml(r.pacing_rules)}</p>
                                    </div>

                                    <div class="p-3 rounded-2xl bg-slate-950/60 border border-slate-800">
                                        <div class="text-[11px] font-bold text-indigo-300 flex items-center gap-1.5 mb-1">
                                            <i data-lucide="check-circle" class="w-3.5 h-3.5"></i>
                                            <span>Deliverable Specs:</span>
                                        </div>
                                        <p class="text-slate-300 text-[11px] leading-relaxed font-mono">${escapeHtml(r.deliverable_specs)}</p>
                                    </div>
                                </div>

                                <!-- Current Client Pains & Winning Skills -->
                                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                                    <div class="p-3 rounded-2xl bg-slate-900/60 border border-slate-800">
                                        <div class="font-bold text-rose-300 text-[11px] mb-1.5 flex items-center gap-1">
                                            <i data-lucide="alert-circle" class="w-3 h-3 text-rose-400"></i>
                                            <span>Why They Are Hiring:</span>
                                        </div>
                                        <ul class="space-y-1 text-[11px] text-slate-400 list-disc list-inside">
                                            ${(r.current_client_pains || []).map(p => `<li>${escapeHtml(p)}</li>`).join('')}
                                        </ul>
                                    </div>
                                    <div class="p-3 rounded-2xl bg-slate-900/60 border border-slate-800">
                                        <div class="font-bold text-emerald-300 text-[11px] mb-1.5 flex items-center gap-1">
                                            <i data-lucide="award" class="w-3 h-3 text-emerald-400"></i>
                                            <span>Winning Skills:</span>
                                        </div>
                                        <ul class="space-y-1 text-[11px] text-slate-400 list-disc list-inside">
                                            ${(r.winning_skills || []).map(s => `<li>${escapeHtml(s)}</li>`).join('')}
                                        </ul>
                                    </div>
                                </div>

                                <!-- Software Stack -->
                                <div class="flex items-center gap-2 pt-1 text-[11px]">
                                    <span class="text-slate-500 font-bold">Stack:</span>
                                    <span class="text-slate-300 font-mono">${escapeHtml(r.software_stack)}</span>
                                </div>
                            </div>

                            <!-- Card Action -->
                            <div class="mt-5 pt-4 border-t border-slate-800/80 flex items-center justify-end">
                                <button onclick="prefillPitchGenerator('${escapeHtml(r.title)}', '${escapeHtml(r.style_category)}')" class="px-4 py-2 rounded-xl bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-500 hover:to-purple-500 text-white font-bold text-xs transition shadow-md shadow-pink-600/20 flex items-center gap-1.5 active:scale-95">
                                    <i data-lucide="sparkles" class="w-3.5 h-3.5"></i>
                                    <span>Craft Pitch for this Niche</span>
                                </button>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    // SUB-TAB 2: PROSPECTING PLAYBOOKS & SEARCH QUERIES
    else if (activeSubTab === 'playbooks') {
        html += `
            <div class="space-y-6">
                <div>
                    <h2 class="text-2xl font-black text-white tracking-tight">Step-by-Step Client Prospecting Playbooks</h2>
                    <p class="text-xs text-slate-400 mt-1">Specific workflows to uncover creators, founders, and local businesses ready to hire</p>
                </div>

                <div class="space-y-6">
                    ${playbooks.map(pb => `
                        <div class="glass-panel rounded-3xl p-6 sm:p-8 border border-slate-800/90 shadow-xl space-y-5">
                            <!-- Playbook Header -->
                            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-800/80">
                                <div class="flex items-center gap-3">
                                    <div class="w-12 h-12 rounded-2xl bg-indigo-500/15 border border-indigo-500/30 flex items-center justify-center text-indigo-400 shrink-0">
                                        <i data-lucide="${pb.icon || 'target'}" class="w-6 h-6"></i>
                                    </div>
                                    <div>
                                        <div class="flex items-center gap-2">
                                            <h3 class="text-xl font-black text-white">${escapeHtml(pb.channel)}</h3>
                                            <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-indigo-500/10 text-indigo-300 border border-indigo-500/30 font-mono">${escapeHtml(pb.difficulty)}</span>
                                        </div>
                                        <p class="text-xs text-pink-400 font-semibold mt-0.5">${escapeHtml(pb.tagline)}</p>
                                    </div>
                                </div>
                                <div class="text-right sm:text-right shrink-0">
                                    <span class="text-[10px] text-slate-500 uppercase font-mono block">Estimated Success</span>
                                    <span class="text-sm font-black text-emerald-400 font-mono">${escapeHtml(pb.conversion_rate)}</span>
                                </div>
                            </div>

                            <!-- Target Criteria -->
                            <div class="p-4 rounded-2xl bg-slate-900/80 border border-slate-800">
                                <div class="text-xs font-bold text-amber-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                                    <i data-lucide="check-square" class="w-4 h-4 text-amber-400"></i>
                                    <span>Who to Target (Exact Criteria):</span>
                                </div>
                                <ul class="space-y-1.5 text-xs text-slate-300 list-disc list-inside">
                                    ${(pb.target_criteria || []).map(c => `<li>${escapeHtml(c)}</li>`).join('')}
                                </ul>
                            </div>

                            <!-- Step-by-Step Execution Workflow -->
                            <div class="space-y-2">
                                <div class="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
                                    <i data-lucide="list-ordered" class="w-4 h-4 text-pink-400"></i>
                                    <span>Execution Blueprint:</span>
                                </div>
                                <div class="grid grid-cols-1 gap-2 text-xs">
                                    ${(pb.step_by_step || []).map((step, idx) => `
                                        <div class="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 flex items-start gap-3">
                                            <span class="w-5 h-5 rounded-full bg-pink-500/20 text-pink-400 font-black text-[10px] flex items-center justify-center shrink-0 mt-0.5 font-mono">${idx + 1}</span>
                                            <p class="text-slate-300 leading-relaxed">${escapeHtml(step.replace(/^\d+\.\s*/, ''))}</p>
                                        </div>
                                    `).join('')}
                                </div>
                            </div>

                            <!-- Live Search Operators (Google / Twitter / LinkedIn) -->
                            <div class="space-y-2">
                                <div class="text-xs font-bold text-indigo-300 uppercase tracking-wider flex items-center gap-1.5">
                                    <i data-lucide="terminal" class="w-4 h-4 text-indigo-400"></i>
                                    <span>Copy-Paste Search Operators:</span>
                                </div>
                                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs font-mono">
                                    ${(pb.search_queries || []).map(sq => `
                                        <div class="p-2.5 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-between gap-2 group hover:border-indigo-500/50 transition">
                                            <span class="text-slate-300 truncate text-[11px] select-all">${escapeHtml(sq)}</span>
                                            <button onclick="copyToClipboard('${escapeHtml(sq).replace(/'/g, "\\'")}', 'Search operator copied!')" class="p-1.5 rounded-lg bg-slate-800 hover:bg-indigo-600 text-slate-400 hover:text-white transition shrink-0 active:scale-90" title="Copy search query">
                                                <i data-lucide="copy" class="w-3.5 h-3.5"></i>
                                            </button>
                                        </div>
                                    `).join('')}
                                </div>
                            </div>

                            <!-- Pro Tips -->
                            <div class="p-3.5 rounded-2xl bg-indigo-950/20 border border-indigo-500/30 text-xs">
                                <div class="font-bold text-indigo-300 mb-1 flex items-center gap-1.5">
                                    <i data-lucide="lightbulb" class="w-4 h-4 text-amber-400"></i>
                                    <span>High-Converting Rules of Thumb:</span>
                                </div>
                                <ul class="space-y-1 text-slate-300 list-disc list-inside text-[11px]">
                                    ${(pb.pro_tips || []).map(pt => `<li>${escapeHtml(pt)}</li>`).join('')}
                                </ul>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    // SUB-TAB 3: AI CUSTOM PITCH GENERATOR
    else if (activeSubTab === 'generator') {
        const prefill = state.clientAcquisition.prefilledNiche || '';
        const generated = state.clientAcquisition.generatedPitch;

        html += `
            <div class="space-y-8">
                <div>
                    <h2 class="text-2xl font-black text-white tracking-tight">AI High-Converting Cold Pitch Generator</h2>
                    <p class="text-xs text-slate-400 mt-1">Generate tailored, objection-proof cold emails & DMs that pitch proof instead of asking for work</p>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
                    <!-- Generator Inputs Form -->
                    <div class="lg:col-span-5 glass-panel rounded-3xl p-6 sm:p-7 border border-slate-800/90 shadow-xl space-y-4">
                        <div class="flex items-center gap-2 pb-3 border-b border-slate-800">
                            <i data-lucide="edit-3" class="w-4 h-4 text-pink-400"></i>
                            <h3 class="font-bold text-white text-sm">Prospect Information</h3>
                        </div>

                        <div>
                            <label class="block text-xs font-bold text-slate-300 mb-1">Target Client / Creator Name <span class="text-rose-400">*</span></label>
                            <input id="pitch-client-name" type="text" placeholder="e.g. Ali Abdaal, Alex Hormozi, Sarah Jenkins" class="w-full bg-slate-900 text-white text-xs py-2.5 px-3.5 rounded-xl border border-slate-700 focus:outline-none focus:border-pink-500 font-medium" />
                        </div>

                        <div>
                            <label class="block text-xs font-bold text-slate-300 mb-1">Channel Name or Niche <span class="text-rose-400">*</span></label>
                            <input id="pitch-client-niche" type="text" value="${escapeHtml(prefill)}" placeholder="e.g. Productivity & Tech Reviews, Real Estate, AI SaaS" class="w-full bg-slate-900 text-white text-xs py-2.5 px-3.5 rounded-xl border border-slate-700 focus:outline-none focus:border-pink-500 font-medium" />
                        </div>

                        <div>
                            <label class="block text-xs font-bold text-slate-300 mb-1">Pitch Strategy / Channel Angle</label>
                            <select id="pitch-type-select" class="w-full bg-slate-900 text-slate-200 text-xs py-2.5 px-3 rounded-xl border border-slate-700 focus:outline-none font-medium">
                                <option value="youtube_sample" selected>🎬 Free 45s Hook Re-edit Sample (YouTube Creators)</option>
                                <option value="founder_repurpose">🎙️ Founder Podcast Repurposing (LinkedIn / X DMs)</option>
                                <option value="short_dm">📱 Quick 30s Viral Short DM (Instagram / Twitter)</option>
                                <option value="upwork">💼 High-Converting Upwork Proposal (Proof-First Angle)</option>
                            </select>
                        </div>

                        <div>
                            <label class="block text-xs font-bold text-slate-300 mb-1">Custom Re-Edit Video Link <span class="text-slate-500">(Optional)</span></label>
                            <input id="pitch-custom-link" type="text" placeholder="e.g. https://drive.google.com/... or Loom link" class="w-full bg-slate-900 text-white text-xs py-2.5 px-3.5 rounded-xl border border-slate-700 focus:outline-none focus:border-pink-500 font-medium font-mono" />
                            <span class="text-[10px] text-slate-500 mt-1 block">Pro Tip: Unlisted Google Drive or Loom preview links get 4x more clicks.</span>
                        </div>

                        <div class="pt-2">
                            <button onclick="handleGeneratePitch()" class="w-full py-3 rounded-xl bg-gradient-to-r from-pink-600 via-purple-600 to-indigo-600 hover:from-pink-500 hover:to-indigo-500 text-white font-bold text-xs transition shadow-lg shadow-pink-600/25 flex items-center justify-center gap-2 active:scale-95">
                                <i data-lucide="sparkles" class="w-4 h-4"></i>
                                <span>Generate Personalized Pitch Script</span>
                            </button>
                        </div>
                    </div>

                    <!-- Generator Output Screen -->
                    <div class="lg:col-span-7 glass-panel rounded-3xl p-6 sm:p-7 border border-slate-800/90 shadow-xl space-y-5">
                        <div class="flex items-center justify-between pb-3 border-b border-slate-800">
                            <div class="flex items-center gap-2">
                                <i data-lucide="mail-check" class="w-4 h-4 text-emerald-400"></i>
                                <h3 class="font-bold text-white text-sm">Generated Cold Pitch Result</h3>
                            </div>
                            ${generated ? `
                                <div class="flex items-center gap-2">
                                    <button onclick="saveCurrentPitchAsLead()" class="px-3 py-1.5 rounded-xl bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-300 border border-emerald-500/40 text-xs font-bold transition flex items-center gap-1.5 active:scale-95" title="Add directly to your Client Outreach Pipeline">
                                        <i data-lucide="user-plus" class="w-3.5 h-3.5"></i>
                                        <span>Save to CRM Pipeline</span>
                                    </button>
                                </div>
                            ` : ''}
                        </div>

                        ${generated ? `
                            <div class="space-y-4">
                                <!-- Subject Line -->
                                <div class="p-3.5 rounded-2xl bg-slate-900 border border-slate-800 space-y-1.5">
                                    <div class="flex items-center justify-between">
                                        <span class="text-[10px] font-bold text-pink-400 uppercase tracking-wider font-mono">Email Subject Line</span>
                                        <button onclick="copyToClipboard('${escapeHtml(generated.subject).replace(/'/g, "\\'")}', 'Subject copied!')" class="text-xs text-slate-400 hover:text-white flex items-center gap-1 transition">
                                            <i data-lucide="copy" class="w-3 h-3"></i>
                                            <span>Copy</span>
                                        </button>
                                    </div>
                                    <div class="text-sm font-bold text-white select-all">${escapeHtml(generated.subject)}</div>
                                </div>

                                <!-- Body -->
                                <div class="p-4 rounded-2xl bg-slate-900 border border-slate-800 space-y-2">
                                    <div class="flex items-center justify-between">
                                        <span class="text-[10px] font-bold text-indigo-400 uppercase tracking-wider font-mono">Pitch Body Copy</span>
                                        <button onclick="copyToClipboard('${escapeHtml(generated.body).replace(/'/g, "\\'").replace(/\n/g, '\\n')}', 'Pitch body copied!')" class="text-xs text-slate-400 hover:text-white flex items-center gap-1 transition">
                                            <i data-lucide="copy" class="w-3 h-3"></i>
                                            <span>Copy Body</span>
                                        </button>
                                    </div>
                                    <div class="text-xs text-slate-200 whitespace-pre-wrap leading-relaxed select-all font-sans bg-slate-950/60 p-3.5 rounded-xl border border-slate-800/80">${escapeHtml(generated.body)}</div>
                                </div>

                                <div class="p-3.5 rounded-2xl bg-emerald-950/20 border border-emerald-500/30 flex items-center justify-between gap-3 text-xs">
                                    <div class="text-emerald-300">
                                        <strong>Ready to send?</strong> Click below to track this outreach in your CRM pipeline.
                                    </div>
                                    <button onclick="saveCurrentPitchAsLead()" class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs transition shadow-md active:scale-95 shrink-0 flex items-center gap-1.5">
                                        <i data-lucide="save" class="w-3.5 h-3.5"></i>
                                        <span>Add to Outreach Leads</span>
                                    </button>
                                </div>
                            </div>
                        ` : `
                            <div class="p-12 text-center text-slate-500 space-y-3">
                                <i data-lucide="send" class="w-10 h-10 mx-auto text-slate-600"></i>
                                <div class="text-sm font-medium text-slate-400">Fill in the prospect details on the left and click Generate.</div>
                                <p class="text-xs text-slate-500 max-w-sm mx-auto">
                                    The script will be customized with non-salesy, value-first copy that highlights your specific hook re-edit sample.
                                </p>
                            </div>
                        `}
                    </div>
                </div>
            </div>
        `;
    }

    // SUB-TAB 4: COLD EMAIL TEMPLATES & OBJECTION HANDLING
    else if (activeSubTab === 'templates') {
        html += `
            <div class="space-y-8">
                <div>
                    <h2 class="text-2xl font-black text-white tracking-tight">Cold Email Vault & Objection Handling Matrix</h2>
                    <p class="text-xs text-slate-400 mt-1">Field-tested outreach templates and exactly what to say when prospects push back</p>
                </div>

                <!-- Cold Email Templates -->
                <div class="space-y-4">
                    <h3 class="text-lg font-bold text-white flex items-center gap-2">
                        <i data-lucide="mail" class="w-4 h-4 text-pink-400"></i>
                        <span>Battle-Tested Cold Email Frameworks</span>
                    </h3>
                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                        ${templates.map(t => `
                            <div class="glass-panel rounded-2xl p-5 border border-slate-800 flex flex-col justify-between space-y-3">
                                <div>
                                    <div class="flex items-center justify-between gap-2 mb-2">
                                        <h4 class="font-black text-white text-sm">${escapeHtml(t.name)}</h4>
                                        <span class="px-2 py-0.5 rounded text-[10px] font-mono bg-pink-500/10 text-pink-300 border border-pink-500/20">${escapeHtml(t.angle)}</span>
                                    </div>
                                    <div class="p-2.5 rounded-xl bg-slate-900 border border-slate-800 mb-2.5">
                                        <span class="text-[10px] text-slate-500 uppercase font-mono block">Subject Line</span>
                                        <span class="text-xs font-bold text-white select-all">${escapeHtml(t.subject)}</span>
                                    </div>
                                    <div class="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 text-xs text-slate-300 whitespace-pre-wrap leading-relaxed font-sans max-h-48 overflow-y-auto no-scrollbar select-all">${escapeHtml(t.body)}</div>
                                </div>
                                <div class="flex items-center justify-end pt-2 border-t border-slate-800/80">
                                    <button onclick="copyToClipboard('${escapeHtml(t.body).replace(/'/g, "\\'").replace(/\n/g, '\\n')}', 'Email template copied!')" class="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-pink-600 text-slate-300 hover:text-white text-xs font-bold transition flex items-center gap-1.5 active:scale-95">
                                        <i data-lucide="copy" class="w-3.5 h-3.5"></i>
                                        <span>Copy Template</span>
                                    </button>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <!-- Objection Handling Matrix -->
                <div class="space-y-4 pt-4">
                    <h3 class="text-lg font-bold text-white flex items-center gap-2">
                        <i data-lucide="shield" class="w-4 h-4 text-emerald-400"></i>
                        <span>Objection Handling Scripts (What to Say When They Say...)</span>
                    </h3>
                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                        ${objections.map(obj => `
                            <div class="glass-panel rounded-2xl p-5 border border-slate-800 space-y-3">
                                <div class="flex items-center justify-between gap-2">
                                    <div class="text-sm font-bold text-rose-300 flex items-center gap-1.5">
                                        <i data-lucide="help-circle" class="w-4 h-4 text-rose-400 shrink-0"></i>
                                        <span>"${escapeHtml(obj.objection)}"</span>
                                    </div>
                                    <span class="px-2 py-0.5 rounded text-[10px] font-mono bg-indigo-500/10 text-indigo-300 border border-indigo-500/30">${escapeHtml(obj.framework)}</span>
                                </div>
                                <div class="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800 text-xs text-slate-200 leading-relaxed font-sans select-all">
                                    ${escapeHtml(obj.script)}
                                </div>
                                <div class="flex justify-end">
                                    <button onclick="copyToClipboard('${escapeHtml(obj.script).replace(/'/g, "\\'")}', 'Script copied!')" class="px-3 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-xs font-bold transition flex items-center gap-1">
                                        <i data-lucide="copy" class="w-3 h-3"></i>
                                        <span>Copy Script</span>
                                    </button>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    // SUB-TAB 5: RETAINER CALCULATOR & ROADMAPS
    else if (activeSubTab === 'calculator') {
        html += `
            <div class="space-y-8">
                <div>
                    <h2 class="text-2xl font-black text-white tracking-tight">Retainer Benchmarks & Monthly Income Roadmaps</h2>
                    <p class="text-xs text-slate-400 mt-1">Realistic workload formulas and daily pitch quotas required to hit your income targets</p>
                </div>

                <!-- Income Roadmaps Grid -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    ${presets.map(ps => `
                        <div class="glass-panel rounded-3xl p-6 border border-slate-800 shadow-xl flex flex-col justify-between hover:border-pink-500/40 transition">
                            <div class="space-y-4">
                                <div class="flex items-center justify-between pb-3 border-b border-slate-800">
                                    <span class="text-xs font-bold text-pink-400 uppercase tracking-wider">${escapeHtml(ps.title)}</span>
                                    <span class="text-2xl font-black text-emerald-400 font-mono">${escapeHtml(ps.target_income)}</span>
                                </div>
                                <div class="space-y-2 text-xs">
                                    <div class="p-3 rounded-2xl bg-slate-900 border border-slate-800">
                                        <span class="text-[10px] text-slate-400 font-bold uppercase block mb-1">Pricing Formula</span>
                                        <p class="text-white font-semibold font-mono text-[11px]">${escapeHtml(ps.formula)}</p>
                                    </div>
                                    <div class="p-3 rounded-2xl bg-slate-900 border border-slate-800">
                                        <span class="text-[10px] text-slate-400 font-bold uppercase block mb-1">Monthly Workload</span>
                                        <p class="text-slate-300 text-[11px]">${escapeHtml(ps.workload)}</p>
                                    </div>
                                    <div class="p-3 rounded-2xl bg-indigo-950/20 border border-indigo-500/30">
                                        <span class="text-[10px] text-indigo-300 font-bold uppercase block mb-1">Daily Pitch Target</span>
                                        <p class="text-indigo-200 text-[11px]">${escapeHtml(ps.daily_pitch_target)}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>

                <!-- Custom Interactive Calculator -->
                <div class="glass-panel rounded-3xl p-6 sm:p-8 border border-slate-800/90 shadow-xl space-y-6">
                    <div class="flex items-center gap-2 pb-3 border-b border-slate-800">
                        <i data-lucide="calculator" class="w-5 h-5 text-emerald-400"></i>
                        <h3 class="text-lg font-black text-white">Custom Retainer Goal Calculator</h3>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                        <div>
                            <label class="block text-xs font-bold text-slate-300 mb-1">Target Monthly Income ($)</label>
                            <input id="calc-target-income" type="number" value="6000" step="500" oninput="updateCustomRetainerCalc()" class="w-full bg-slate-900 text-white text-sm py-2.5 px-3 rounded-xl border border-slate-700 font-mono font-bold" />
                        </div>
                        <div>
                            <label class="block text-xs font-bold text-slate-300 mb-1">Average Retainer Price per Client ($)</label>
                            <input id="calc-retainer-price" type="number" value="1500" step="250" oninput="updateCustomRetainerCalc()" class="w-full bg-slate-900 text-white text-sm py-2.5 px-3 rounded-xl border border-slate-700 font-mono font-bold" />
                        </div>
                        <div>
                            <label class="block text-xs font-bold text-slate-300 mb-1">Pitches Sent Per Day</label>
                            <input id="calc-daily-pitches" type="number" value="8" step="1" oninput="updateCustomRetainerCalc()" class="w-full bg-slate-900 text-white text-sm py-2.5 px-3 rounded-xl border border-slate-700 font-mono font-bold" />
                        </div>
                    </div>

                    <!-- Calculator Output Display -->
                    <div id="calc-results-display" class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
                        <div class="p-3.5 rounded-2xl bg-slate-900 border border-slate-800 text-center">
                            <span class="text-[10px] text-slate-500 uppercase font-mono block">Clients Needed</span>
                            <span id="res-clients-needed" class="text-xl font-black text-white font-mono">4 Clients</span>
                        </div>
                        <div class="p-3.5 rounded-2xl bg-slate-900 border border-slate-800 text-center">
                            <span class="text-[10px] text-slate-500 uppercase font-mono block">Monthly Outreach Volume</span>
                            <span id="res-monthly-pitches" class="text-xl font-black text-indigo-400 font-mono">160 Pitches</span>
                        </div>
                        <div class="p-3.5 rounded-2xl bg-slate-900 border border-slate-800 text-center">
                            <span class="text-[10px] text-slate-500 uppercase font-mono block">Expected Positive Replies</span>
                            <span id="res-expected-replies" class="text-xl font-black text-pink-400 font-mono">5 - 8 Replies</span>
                        </div>
                        <div class="p-3.5 rounded-2xl bg-slate-900 border border-slate-800 text-center">
                            <span class="text-[10px] text-slate-500 uppercase font-mono block">Estimated Time to Hit Goal</span>
                            <span id="res-estimated-days" class="text-xl font-black text-emerald-400 font-mono">~30 Days</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // SUB-TAB 6: CLIENT OUTREACH CRM PIPELINE
    else if (activeSubTab === 'crm') {
        const filterStatus = state.clientAcquisition.filterLeadStatus || 'all';
        const filteredLeads = filterStatus === 'all' ? leads : leads.filter(l => l.status === filterStatus);

        const statusOptions = ['Targeted', 'Sample Sent', 'Call Booked', 'Closed Retainer', 'Follow-Up Needed', 'Declined'];

        html += `
            <div class="space-y-6">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div>
                        <h2 class="text-2xl font-black text-white tracking-tight">Video Client Outreach Pipeline & CRM</h2>
                        <p class="text-xs text-slate-400 mt-1">Track prospect pitches, re-edited hook samples, call schedules, and closed retainers</p>
                    </div>
                    <button onclick="toggleAddLeadDrawer()" class="px-4 py-2.5 rounded-xl bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-500 hover:to-purple-500 text-white font-bold text-xs transition shadow-lg shadow-pink-600/20 flex items-center gap-1.5 active:scale-95 shrink-0">
                        <i data-lucide="user-plus" class="w-4 h-4"></i>
                        <span>+ Add New Outreach Lead</span>
                    </button>
                </div>

                <!-- Pipeline Summary Cards -->
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    <div class="p-3.5 rounded-2xl bg-slate-900 border border-slate-800">
                        <span class="text-[10px] font-bold text-slate-400 uppercase font-mono">Total Pitched</span>
                        <div class="text-2xl font-black text-white font-mono mt-0.5">${totalLeads}</div>
                    </div>
                    <div class="p-3.5 rounded-2xl bg-slate-900 border border-slate-800">
                        <span class="text-[10px] font-bold text-pink-400 uppercase font-mono">Samples Delivered</span>
                        <div class="text-2xl font-black text-pink-300 font-mono mt-0.5">${samplesSent}</div>
                    </div>
                    <div class="p-3.5 rounded-2xl bg-slate-900 border border-slate-800">
                        <span class="text-[10px] font-bold text-indigo-400 uppercase font-mono">Calls Booked</span>
                        <div class="text-2xl font-black text-indigo-300 font-mono mt-0.5">${callsBooked}</div>
                    </div>
                    <div class="p-3.5 rounded-2xl bg-slate-900 border border-slate-800">
                        <span class="text-[10px] font-bold text-emerald-400 uppercase font-mono">Retainers Closed</span>
                        <div class="text-2xl font-black text-emerald-400 font-mono mt-0.5">${closedRetainers}</div>
                    </div>
                </div>

                <!-- Add Lead Drawer (Collapsible) -->
                <div id="add-lead-drawer" class="hidden glass-panel rounded-3xl p-6 border border-pink-500/40 shadow-2xl space-y-4">
                    <div class="flex items-center justify-between pb-3 border-b border-slate-800">
                        <h4 class="font-black text-white text-sm flex items-center gap-2">
                            <i data-lucide="plus-circle" class="w-4 h-4 text-pink-400"></i>
                            <span>Add Prospective Client to Pipeline</span>
                        </h4>
                        <button onclick="toggleAddLeadDrawer()" class="text-slate-400 hover:text-white p-1">
                            <i data-lucide="x" class="w-4 h-4"></i>
                        </button>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                        <div>
                            <label class="block font-bold text-slate-300 mb-1">Client / Creator Name <span class="text-rose-400">*</span></label>
                            <input id="new-lead-name" type="text" placeholder="e.g. Graham Stephan, Acme Software" class="w-full bg-slate-900 text-white p-2.5 rounded-xl border border-slate-700 focus:outline-none focus:border-pink-500" />
                        </div>
                        <div>
                            <label class="block font-bold text-slate-300 mb-1">Channel / Website / Video Link</label>
                            <input id="new-lead-channel" type="text" placeholder="e.g. youtube.com/@channel or website" class="w-full bg-slate-900 text-white p-2.5 rounded-xl border border-slate-700 focus:outline-none focus:border-pink-500" />
                        </div>
                        <div>
                            <label class="block font-bold text-slate-300 mb-1">Client Niche</label>
                            <input id="new-lead-niche" type="text" placeholder="e.g. Finance, SaaS, Podcasting" class="w-full bg-slate-900 text-white p-2.5 rounded-xl border border-slate-700 focus:outline-none focus:border-pink-500" />
                        </div>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                        <div>
                            <label class="block font-bold text-slate-300 mb-1">Outreach Channel</label>
                            <select id="new-lead-outreach-channel" class="w-full bg-slate-900 text-slate-200 p-2.5 rounded-xl border border-slate-700">
                                <option value="Email">Email</option>
                                <option value="Twitter/X DM">Twitter / X DM</option>
                                <option value="LinkedIn">LinkedIn</option>
                                <option value="Instagram DM">Instagram DM</option>
                                <option value="Upwork">Upwork</option>
                            </select>
                        </div>
                        <div>
                            <label class="block font-bold text-slate-300 mb-1">Initial Status</label>
                            <select id="new-lead-status" class="w-full bg-slate-900 text-slate-200 p-2.5 rounded-xl border border-slate-700">
                                <option value="Targeted">Targeted</option>
                                <option value="Sample Sent">Sample Sent</option>
                                <option value="Call Booked">Call Booked</option>
                                <option value="Follow-Up Needed">Follow-Up Needed</option>
                                <option value="Closed Retainer">Closed Retainer</option>
                            </select>
                        </div>
                        <div>
                            <label class="block font-bold text-slate-300 mb-1">Next Follow-Up Date</label>
                            <input id="new-lead-followup" type="date" class="w-full bg-slate-900 text-slate-200 p-2.5 rounded-xl border border-slate-700" />
                        </div>
                    </div>

                    <div>
                        <label class="block text-xs font-bold text-slate-300 mb-1">Notes / Context (Bottlenecks, Video Feedback)</label>
                        <textarea id="new-lead-notes" rows="2" placeholder="e.g. Watched their video on AI Tools. First 30s has dead silence. Sent unlisted 45s re-edit on Loom." class="w-full bg-slate-900 text-white text-xs p-3 rounded-xl border border-slate-700 focus:outline-none focus:border-pink-500"></textarea>
                    </div>

                    <div class="flex items-center justify-end gap-2 pt-2 border-t border-slate-800">
                        <button onclick="toggleAddLeadDrawer()" class="px-4 py-2 rounded-xl text-xs font-bold text-slate-400 hover:text-white">Cancel</button>
                        <button onclick="handleAddNewLead()" class="px-5 py-2.5 rounded-xl bg-pink-600 hover:bg-pink-500 text-white font-bold text-xs shadow-md transition active:scale-95">Save Lead to CRM</button>
                    </div>
                </div>

                <!-- Status Filter Bar -->
                <div class="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-1">
                    <span class="text-xs font-bold text-slate-500 uppercase tracking-wider mr-2 font-mono">Filter:</span>
                    <button onclick="filterLeadsByStatus('all')" class="px-3 py-1.5 rounded-xl text-xs font-bold transition ${filterStatus === 'all' ? 'bg-pink-600 text-white' : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'}">All (${totalLeads})</button>
                    ${statusOptions.map(st => {
                        const count = leads.filter(l => l.status === st).length;
                        return `
                            <button onclick="filterLeadsByStatus('${st}')" class="px-3 py-1.5 rounded-xl text-xs font-bold transition whitespace-nowrap ${filterStatus === st ? 'bg-pink-600 text-white' : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'}">${st} (${count})</button>
                        `;
                    }).join('')}
                </div>

                <!-- Leads Table / Cards List -->
                ${filteredLeads.length > 0 ? `
                    <div class="glass-panel rounded-3xl overflow-hidden border border-slate-800/90 shadow-xl">
                        <div class="overflow-x-auto">
                            <table class="w-full text-left text-xs border-collapse">
                                <thead>
                                    <tr class="border-b border-slate-800/80 bg-slate-950/60 text-slate-400 font-mono text-[10px] uppercase">
                                        <th class="py-3.5 px-4 font-bold">Client / Creator</th>
                                        <th class="py-3.5 px-4 font-bold">Niche / Channel</th>
                                        <th class="py-3.5 px-4 font-bold">Outreach Channel</th>
                                        <th class="py-3.5 px-4 font-bold">Status Pipeline</th>
                                        <th class="py-3.5 px-4 font-bold">Follow-Up</th>
                                        <th class="py-3.5 px-4 font-bold">Notes</th>
                                        <th class="py-3.5 px-4 font-bold text-right">Actions</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-800/60 text-slate-300">
                                    ${filteredLeads.map(lead => {
                                        const statusColors = {
                                            'Targeted': 'bg-slate-800 text-slate-300 border-slate-700',
                                            'Sample Sent': 'bg-pink-500/10 text-pink-300 border-pink-500/30',
                                            'Call Booked': 'bg-indigo-500/10 text-indigo-300 border-indigo-500/30',
                                            'Closed Retainer': 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30 font-bold',
                                            'Follow-Up Needed': 'bg-amber-500/10 text-amber-300 border-amber-500/30',
                                            'Declined': 'bg-rose-500/10 text-rose-300 border-rose-500/30'
                                        };
                                        const badgeClass = statusColors[lead.status] || 'bg-slate-800 text-slate-300 border-slate-700';

                                        return `
                                            <tr class="hover:bg-slate-850/40 transition group">
                                                <td class="py-3 px-4 font-bold text-white">
                                                    <div>${escapeHtml(lead.client_name)}</div>
                                                    ${lead.channel_or_website ? `
                                                        <a href="${escapeHtml(lead.channel_or_website)}" target="_blank" class="text-[10px] text-pink-400 hover:underline truncate max-w-xs block font-mono">${escapeHtml(lead.channel_or_website)}</a>
                                                    ` : ''}
                                                </td>
                                                <td class="py-3 px-4 font-mono text-[11px] text-slate-300">
                                                    ${escapeHtml(lead.client_niche || 'YouTube')}
                                                </td>
                                                <td class="py-3 px-4">
                                                    <span class="px-2 py-0.5 rounded text-[10px] bg-slate-900 border border-slate-800 font-mono">${escapeHtml(lead.outreach_channel || 'Email')}</span>
                                                </td>
                                                <td class="py-3 px-4">
                                                    <select onchange="updateLeadStatus(${lead.id}, this.value)" class="text-[11px] font-semibold py-1 px-2 rounded-lg border focus:outline-none cursor-pointer ${badgeClass}">
                                                        ${statusOptions.map(st => `
                                                            <option value="${st}" ${lead.status === st ? 'selected' : ''}>${st}</option>
                                                        `).join('')}
                                                    </select>
                                                </td>
                                                <td class="py-3 px-4 font-mono text-[11px]">
                                                    ${lead.followup_date ? `
                                                        <span class="text-amber-300 flex items-center gap-1">
                                                            <i data-lucide="calendar" class="w-3 h-3 text-amber-400"></i>
                                                            <span>${escapeHtml(lead.followup_date)}</span>
                                                        </span>
                                                    ` : '<span class="text-slate-600">—</span>'}
                                                </td>
                                                <td class="py-3 px-4 text-xs text-slate-400 max-w-xs truncate" title="${escapeHtml(lead.notes || '')}">
                                                    ${escapeHtml(lead.notes || '—')}
                                                </td>
                                                <td class="py-3 px-4 text-right">
                                                    <button onclick="deleteLead(${lead.id})" class="p-1.5 rounded-lg text-slate-500 hover:text-rose-400 hover:bg-slate-800 transition active:scale-90" title="Delete Lead">
                                                        <i data-lucide="trash-2" class="w-4 h-4"></i>
                                                    </button>
                                                </td>
                                            </tr>
                                        `;
                                    }).join('')}
                                </tbody>
                            </table>
                        </div>
                    </div>
                ` : `
                    <div class="glass-panel rounded-3xl p-12 text-center border border-slate-800 space-y-3">
                        <i data-lucide="users" class="w-10 h-10 mx-auto text-slate-600"></i>
                        <h4 class="text-sm font-bold text-white">No leads found in this view</h4>
                        <p class="text-xs text-slate-500 max-w-sm mx-auto">
                            Use the <strong>AI Custom Pitch Generator</strong> or click <strong>+ Add New Outreach Lead</strong> to start logging your client outreach.
                        </p>
                    </div>
                `}
            </div>
        `;
    }

    container.innerHTML = html;
    if (window.lucide) lucide.createIcons();
}

function toggleAddLeadDrawer() {
    const drawer = document.getElementById('add-lead-drawer');
    if (!drawer) return;
    drawer.classList.toggle('hidden');
}

function filterLeadsByStatus(statusKey) {
    if (!state.clientAcquisition) state.clientAcquisition = {};
    state.clientAcquisition.filterLeadStatus = statusKey;
    renderClientAcquisitionUI();
}

function updateCustomRetainerCalc() {
    const incInput = document.getElementById('calc-target-income');
    const retInput = document.getElementById('calc-retainer-price');
    const pitInput = document.getElementById('calc-daily-pitches');

    const targetIncome = Math.max(parseFloat(incInput ? incInput.value : 6000) || 6000, 100);
    const retainerPrice = Math.max(parseFloat(retInput ? retInput.value : 1500) || 1500, 100);
    const dailyPitches = Math.max(parseFloat(pitInput ? pitInput.value : 8) || 8, 1);

    const clientsNeeded = Math.ceil(targetIncome / retainerPrice);
    const monthlyPitches = Math.round(dailyPitches * 20); // 20 working days
    const minReplies = Math.max(Math.round(monthlyPitches * 0.03), 1);
    const maxReplies = Math.max(Math.round(monthlyPitches * 0.06), 2);

    // Assuming 2.5% overall close rate on personalized pitches
    const totalPitchesNeeded = Math.ceil(clientsNeeded / 0.025);
    const daysNeeded = Math.ceil(totalPitchesNeeded / dailyPitches);

    const elClients = document.getElementById('res-clients-needed');
    const elMonthly = document.getElementById('res-monthly-pitches');
    const elReplies = document.getElementById('res-expected-replies');
    const elDays = document.getElementById('res-estimated-days');

    if (elClients) elClients.innerText = `${clientsNeeded} Clients`;
    if (elMonthly) elMonthly.innerText = `${monthlyPitches} Pitches/mo`;
    if (elReplies) elReplies.innerText = `${minReplies} - ${maxReplies} Replies`;
    if (elDays) elDays.innerText = `~${daysNeeded} Days`;
}

'''

with open('static/js/app.js', 'a', encoding='utf-8') as f:
    f.write('\n' + js_code)

print("Successfully appended client acquisition logic to static/js/app.js!")
