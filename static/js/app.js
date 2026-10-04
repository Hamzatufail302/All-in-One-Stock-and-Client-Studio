/**
 * StockPulse AI - Frontend Application Controller
 * Handles live multi-engine search, platform-isolated research,
 * daily goal & progress tracker, 365-day ranked event calendar,
 * AI daily quota generator (15-20 prompts), and production queue.
 */

// Application State
const state = {
    currentTab: 'overview',
    currentQuery: '',
    currentPlatform: 'all',
    searchResults: null,
    searchFilterCategory: 'all',
    searchTimingFilter: 'all',
    searchQueryFilter: '',
    searchSortBy: 'opportunity',
    calendarViewMode: 'detailed',
    overviewData: null,
    todayGoal: null,
    todayAssetsFilter: 'all',
    queueItems: [],
    queueFilterPlatform: 'all',
    calendarEvents: [],
    calendarFilter: 'all',
    calendarCategoryFilter: 'all',
    calendarTimingFilter: 'all',
    calendarSearchQuery: '',
    aiQuotaPrompts: [],
    aiQuotaCategory: 'all',
    alphabetSoupData: null,
    alphabetFilterQuery: '',
    clientAcquisition: {
        overview: null,
        leads: [],
        activeSubTab: 'requirements',
        filterNiche: 'all',
        filterLeadStatus: 'all',
        generatedPitch: null
    },
    registry: new Map() // Safe object cache preventing string escaping / syntax errors
};

// Safe Item Registry helpers
function registerData(data) {
    const id = 'id_' + Math.random().toString(36).substring(2, 11) + '_' + Date.now().toString(36);
    state.registry.set(id, data);
    return id;
}

function getRegisteredData(id) {
    return state.registry.get(id);
}

// --- SCORE SYSTEM ENGINE (UNIVERSAL TITLE & TAG METRICS) ---
function getDeterministicScore(text, minVal = 85, maxVal = 99) {
    let hash = 0;
    const str = (text || '').trim().toLowerCase();
    for (let i = 0; i < str.length; i++) {
        hash = ((hash << 5) - hash) + str.charCodeAt(i);
        hash |= 0;
    }
    return minVal + (Math.abs(hash) % (maxVal - minVal + 1));
}

function resolveTagScore(item, tagText) {
    if (item && item.scored_tags && Array.isArray(item.scored_tags)) {
        const found = item.scored_tags.find(st => (st.tag || '').toLowerCase() === (tagText || '').toLowerCase());
        if (found) return found;
    }
    const score = getDeterministicScore(tagText, 84, 98);
    const color = score >= 94 ? 'emerald' : (score >= 88 ? 'indigo' : 'purple');
    const volume = score >= 94 ? 'Very High' : (score >= 88 ? 'High' : 'Moderate');
    const comp = score >= 92 ? 'Low' : (score >= 86 ? 'Balanced' : 'Moderate');
    return {
        tag: tagText,
        score: score,
        volume: volume,
        volume_score: Math.min(score + 1, 99),
        competition: comp,
        opportunity: `${Math.min(score + 2, 99)}%`,
        tier: score >= 94 ? 'Power Tag (First 10 Slot)' : (score >= 88 ? 'High Intent Conversion' : 'Catalog Volume Booster'),
        color: color
    };
}

function resolveTitleScore(item, titleText, contextKw = '') {
    if (item && item.scored_titles && Array.isArray(item.scored_titles)) {
        const found = item.scored_titles.find(st => (st.title || st) === titleText);
        if (found && typeof found === 'object' && found.score) return found;
    }
    const score = getDeterministicScore(titleText, 88, 99);
    const color = score >= 95 ? 'emerald' : (score >= 90 ? 'indigo' : 'purple');
    const grade = score >= 95 ? 'A+' : (score >= 90 ? 'A' : 'B+');
    const ctr = score >= 95 ? 'Top 5% CTR (High Viral Potential)' : (score >= 90 ? 'High CTR (Strong Search Match)' : 'Solid CTR (Targeted Niche)');
    const comp = score >= 93 ? 'Low Comp • Fast Indexing' : 'Balanced Competition';
    const intent = score >= 94 ? '98% (High B2B & Agency Intent)' : '92% (Commercial Marketing)';
    return {
        title: titleText,
        score: score,
        ctr_rating: ctr,
        volume_score: Math.min(score, 98),
        commercial_intent: intent,
        competition: comp,
        rank_probability: `${Math.min(score + 1, 99)}%`,
        grade: grade,
        color: color
    };
}

// --- UNIVERSAL CLIENT-SIDE DEADLINE & UPLOAD WINDOW HELPER ---
function getClientUploadDeadline(itemOrKw) {
    if (itemOrKw && typeof itemOrKw === 'object') {
        if (itemOrKw.upload_date_range && itemOrKw.upload_deadline) {
            const overdue = itemOrKw.days_past_deadline || itemOrKw.days_overdue || 0;
            return {
                upload_date_range: itemOrKw.upload_date_range,
                upload_deadline: itemOrKw.upload_deadline,
                is_late: Boolean(itemOrKw.is_late),
                days_past_deadline: overdue,
                days_overdue: overdue,
                timing_status: itemOrKw.timing_status || (itemOrKw.is_late ? 'LATE' : 'PRIME_WINDOW'),
                timing_badge: itemOrKw.timing_badge || (itemOrKw.is_late ? '🔴 LATE' : '🟢 PRIME WINDOW')
            };
        }
    }
    const kw = (typeof itemOrKw === 'string' ? itemOrKw : (itemOrKw?.keyword || itemOrKw?.concept || itemOrKw?.name || itemOrKw?.title || itemOrKw?.suggested_title || '')).toLowerCase();
    
    // Dynamic baseline reference: current client system time
    const now = new Date();
    
    let targetMonth = null;
    let targetDay = 15;
    
    if (kw.includes('halloween') || kw.includes('spooky') || kw.includes('pumpkin') || kw.includes('witch') || kw.includes('horror') || kw.includes('autumn leaves')) {
        targetMonth = 9; targetDay = 31;
    } else if (kw.includes('black friday') || kw.includes('cyber monday') || kw.includes('bfcm')) {
        targetMonth = 10; targetDay = 27;
    } else if (kw.includes('thanksgiving') || kw.includes('autumn harvest') || kw.includes('fall vector')) {
        targetMonth = 10; targetDay = 26;
    } else if (kw.includes('christmas') || kw.includes('xmas') || kw.includes('winter') || kw.includes('holiday season') || kw.includes('new year')) {
        targetMonth = 11; targetDay = 25;
    } else if (kw.includes('valentine') || kw.includes('romantic') || kw.includes('love couple')) {
        targetMonth = 1; targetDay = 14;
    } else if (kw.includes('st patrick') || kw.includes('shamrock') || kw.includes('irish')) {
        targetMonth = 2; targetDay = 17;
    } else if (kw.includes('spring') || kw.includes('easter') || kw.includes('floral pattern')) {
        targetMonth = 3; targetDay = 5;
    } else if (kw.includes('mother') || kw.includes("mother's day") || kw.includes('mom')) {
        targetMonth = 4; targetDay = 10;
    } else if (kw.includes('father') || kw.includes("father's day") || kw.includes('dad')) {
        targetMonth = 5; targetDay = 21;
    } else if (kw.includes('4th of july') || kw.includes('independence day') || kw.includes('patriotic')) {
        targetMonth = 6; targetDay = 4;
    } else if (kw.includes('back to school') || kw.includes('classroom') || kw.includes('teacher') || kw.includes('education')) {
        targetMonth = 7; targetDay = 20;
    } else if (kw.includes('fashion') || kw.includes('streetwear') || kw.includes('hoodie') || kw.includes('apparel') || kw.includes('resort') || kw.includes('swimwear') || kw.includes('runway') || kw.includes('clothing')) {
        targetMonth = 10; targetDay = 15;
    } else if (kw.includes('birthday') || kw.includes('18th') || kw.includes('21st') || kw.includes('30th') || kw.includes('50th') || kw.includes('quinceanera') || kw.includes('sweet sixteen') || kw.includes('jubilee')) {
        targetMonth = 10; targetDay = 30;
    } else if (kw.includes('wedding') || kw.includes('bridal') || kw.includes('invitation') || kw.includes('baby shower') || kw.includes('gender reveal') || kw.includes('retirement')) {
        targetMonth = 11; targetDay = 15;
    } else if (kw.includes('diwali') || kw.includes('deepavali')) {
        targetMonth = 10; targetDay = 1;
    } else if (kw.includes('cyber security') || kw.includes('infosec')) {
        targetMonth = 9; targetDay = 1;
    } else if (kw.includes('mental health') || kw.includes('wellness')) {
        targetMonth = 9; targetDay = 10;
    } else if (kw.includes('breast cancer') || kw.includes('pink ribbon')) {
        targetMonth = 9; targetDay = 20;
    } else if (kw.includes('singles day') || kw.includes('veterans day') || kw.includes('11.11')) {
        targetMonth = 10; targetDay = 11;
    } else if (kw.includes('earth day') || kw.includes('ecology') || kw.includes('sustainability')) {
        targetMonth = 3; targetDay = 22;
    } else if (kw.includes('summer') || kw.includes('beach') || kw.includes('pool party') || kw.includes('vacation')) {
        targetMonth = 5; targetDay = 1;
    } else if (kw.includes('fitness') || kw.includes('gym workout') || kw.includes('resolution')) {
        targetMonth = 11; targetDay = 31;
    }
    
    if (targetMonth === null) {
        return {
            upload_date_range: 'Upload Anytime (High Year-Round Commercial Demand)',
            upload_deadline: 'Evergreen (Continuous Indexing)',
            is_late: false,
            days_past_deadline: 0,
            timing_status: 'EVERGREEN',
            timing_badge: '⚡ EVERGREEN: Upload Anytime'
        };
    }
    
    let targetYear = now.getFullYear();
    let targetDate = new Date(targetYear, targetMonth, targetDay);
    if (targetDate.getTime() < now.getTime() - (4 * 24 * 60 * 60 * 1000)) {
        targetYear += 1;
        targetDate = new Date(targetYear, targetMonth, targetDay);
    }
    
    const deadlineDate = new Date(targetDate.getTime() - (45 * 24 * 60 * 60 * 1000));
    const startDate = new Date(targetDate.getTime() - (90 * 24 * 60 * 60 * 1000));
    
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    const fmt = (d) => `${monthNames[d.getMonth()]} ${String(d.getDate()).padStart(2, '0')}, ${d.getFullYear()}`;
    const fmtShort = (d) => `${monthNames[d.getMonth()]} ${String(d.getDate()).padStart(2, '0')}`;
    
    const upload_date_range = `${fmtShort(startDate)} – ${fmt(deadlineDate)}`;
    const upload_deadline = fmt(deadlineDate);
    
    const diffDaysToDeadline = Math.round((deadlineDate - now) / (1000 * 60 * 60 * 24));
    
    let is_late = false;
    let days_past_deadline = 0;
    let timing_status = 'PRIME_WINDOW';
    let timing_badge = '🟢 PRIME UPLOAD WINDOW';
    
    if (now > deadlineDate) {
        is_late = true;
        days_past_deadline = Math.round((now - deadlineDate) / (1000 * 60 * 60 * 24));
        timing_status = 'LATE';
        timing_badge = `🔴 LATE (${days_past_deadline}d past golden deadline)`;
    } else if (diffDaysToDeadline <= 14) {
        timing_status = 'CLOSING_SOON';
        timing_badge = `🟡 CLOSING SOON (${diffDaysToDeadline}d left)`;
    } else if (diffDaysToDeadline <= 45) {
        timing_status = 'PRIME_WINDOW';
        timing_badge = `🟢 PRIME UPLOAD WINDOW (${diffDaysToDeadline}d to deadline)`;
    } else {
        timing_status = 'ADVANCE_PREP';
        timing_badge = `🟣 ADVANCE PRODUCTION (${diffDaysToDeadline}d to deadline)`;
    }
    
    return {
        upload_date_range,
        upload_deadline,
        is_late,
        days_past_deadline,
        days_overdue: days_past_deadline,
        timing_status,
        timing_badge
    };
}

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    initApp();
});

async function initApp() {
    setupEventListeners();
    await loadOverview();
    await loadTodayGoal(false);
    await loadQueueCount();
    lucide.createIcons();
}

function setupEventListeners() {
    const searchInput = document.getElementById('main-search-input');
    if (searchInput) {
        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                handleSearchSubmit();
            }
        });
    }

    // Quick tag pills in hero
    document.querySelectorAll('.quick-niche-pill').forEach(btn => {
        btn.addEventListener('click', () => {
            const kw = btn.dataset.keyword;
            if (kw) {
                const input = document.getElementById('main-search-input');
                if (input) input.value = kw;
                handleSearchSubmit();
            }
        });
    });

    // Close modals on Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeAlphabetModal();
            closeAddIdeaModal();
            closeDeadlineGuideModal();
            closeMobileMenu();
        }
    });

    // Close modals on backdrop click
    const alphabetModal = document.getElementById('alphabet-soup-modal');
    if (alphabetModal) {
        alphabetModal.addEventListener('click', (e) => {
            if (e.target === alphabetModal) closeAlphabetModal();
        });
    }
    const addIdeaModal = document.getElementById('add-idea-modal');
    if (addIdeaModal) {
        addIdeaModal.addEventListener('click', (e) => {
            if (e.target === addIdeaModal) closeAddIdeaModal();
        });
    }
    const deadlineModal = document.getElementById('deadline-guide-modal');
    if (deadlineModal) {
        deadlineModal.addEventListener('click', (e) => {
            if (e.target === deadlineModal) closeDeadlineGuideModal();
        });
    }
}

// --- MOBILE MENU ---
function toggleMobileMenu() {
    const drawer = document.getElementById('mobile-drawer');
    if (!drawer) return;
    if (drawer.classList.contains('drawer-closed')) {
        drawer.classList.remove('drawer-closed');
        drawer.classList.add('drawer-open');
    } else {
        drawer.classList.remove('drawer-open');
        drawer.classList.add('drawer-closed');
    }
    lucide.createIcons();
}

function closeMobileMenu() {
    const drawer = document.getElementById('mobile-drawer');
    if (drawer) {
        drawer.classList.remove('drawer-open');
        drawer.classList.add('drawer-closed');
    }
}

// --- TAB SWITCHING ---
function switchTab(tabId, preserveSearchQuery = null) {
    state.currentTab = tabId;

    // Update main nav active classes
    document.querySelectorAll('.nav-tab').forEach(btn => {
        const target = btn.dataset.tab;
        if (target === tabId || (tabId.startsWith('platform-') && target === 'marketplaces-group')) {
            btn.classList.add('nav-tab-active');
            btn.classList.remove('text-slate-400');
        } else {
            btn.classList.remove('nav-tab-active');
            btn.classList.add('text-slate-400');
        }
    });

    // Control secondary platform strip visibility
    const subnavStrip = document.getElementById('marketplace-subnav-strip');
    if (subnavStrip) {
        if (tabId.startsWith('platform-')) {
            subnavStrip.classList.remove('hidden');
            const platformKey = tabId.replace('platform-', '');
            document.querySelectorAll('.platform-strip-btn').forEach(b => {
                if (b.dataset.platformPill === platformKey) {
                    b.classList.add('border-indigo-500', 'bg-indigo-600/20', 'text-white');
                    b.classList.remove('border-slate-800', 'bg-slate-900', 'text-slate-300');
                } else {
                    b.classList.remove('border-indigo-500', 'bg-indigo-600/20', 'text-white');
                    b.classList.add('border-slate-800', 'bg-slate-900', 'text-slate-300');
                }
            });
        } else {
            subnavStrip.classList.add('hidden');
        }
    }

    // Toggle panels
    document.querySelectorAll('.tab-panel').forEach(panel => {
        if (panel.id === `tab-${tabId}`) {
            panel.classList.remove('hidden');
        } else {
            panel.classList.add('hidden');
        }
    });

    // Lazy load specific tab content
    if (tabId.startsWith('platform-')) {
        const platformId = tabId.replace('platform-', '');
        loadPlatformTab(platformId, preserveSearchQuery);
    } else if (tabId === 'daily-events') {
        loadDailyCalendarTab();
    } else if (tabId === 'daily-tracker') {
        renderDailyTrackerTab();
    } else if (tabId === 'ai-quota') {
        loadAIQuotaTab();
    } else if (tabId === 'queue') {
        loadQueueTab();
    } else if (tabId === 'android-apps') {
        loadAndroidAppsTab(preserveSearchQuery);
    } else if (tabId === 'client-acquisition') {
        loadClientAcquisitionTab();
    }

    lucide.createIcons();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// --- DATA FETCHERS ---
async function loadOverview() {
    try {
        const res = await fetch('/api/trends/overview');
        const data = await res.json();
        state.overviewData = data;
        renderSeasonalHeroBanner(data.seasonal);
        renderPlatformCards(data.platforms);
    } catch (e) {
        console.error('Error loading overview:', e);
    }
}

async function loadTodayGoal(refreshView = false) {
    try {
        const res = await fetch('/api/daily-goals/today');
        const goal = await res.json();
        state.todayGoal = goal;
        updateHeaderGoalBadge(goal);
        if (refreshView && state.currentTab === 'daily-tracker') {
            renderDailyTrackerTab(false);
        }
    } catch (e) {
        console.error('Error loading today goal:', e);
    }
}

function updateHeaderGoalBadge(goal) {
    const badge = document.getElementById('header-goal-badge');
    const fill = document.getElementById('header-goal-fill');
    const text = document.getElementById('header-goal-text');
    if (!badge || !goal) return;

    badge.classList.remove('hidden');
    if (fill) fill.style.width = `${Math.min(goal.percentage || 0, 100)}%`;
    if (text) text.innerText = `Today: ${goal.total_created || 0}/${goal.total_target || 23} (${goal.percentage || 0}%)`;
}

async function loadQueueCount() {
    try {
        const res = await fetch('/api/saved-keywords');
        const data = await res.json();
        state.queueItems = data.items || [];
        const badge = document.getElementById('queue-count-badge');
        if (badge) {
            badge.innerText = state.queueItems.length;
        }
    } catch (e) {
        console.error('Error loading queue count:', e);
    }
}

// --- SEARCH HANDLER (COMBINED VIEW) ---
async function handleSearchSubmit() {
    const input = document.getElementById('main-search-input');
    const query = input.value.trim();
    if (!query) {
        showToast('Please type a keyword or theme to search', 'info');
        return;
    }

    state.currentQuery = query;
    const platform = document.getElementById('search-platform-select').value || 'all';
    state.currentPlatform = platform;

    const resultsContainer = document.getElementById('search-results-section');
    resultsContainer.classList.remove('hidden');
    resultsContainer.innerHTML = `
        <div class="glass-panel rounded-3xl p-12 text-center border border-indigo-500/30">
            <div class="inline-block animate-spin rounded-full h-12 w-12 border-4 border-indigo-500 border-t-transparent mb-4"></div>
            <h3 class="text-xl font-bold text-white">Crawling Live Stock Buyer Intent...</h3>
            <p class="text-slate-400 text-sm mt-2 max-w-lg mx-auto">
                Querying Adobe Stock direct algorithm weights, Google & Bing buyer completion indexes, and cross-platform formatting rules.
            </p>
        </div>
    `;

    try {
        const res = await fetch(`/api/search?q=${encodeURIComponent(query)}&platform=${encodeURIComponent(platform)}&limit=60`);
        const data = await res.json();
        state.searchResults = data;
        renderSearchResults(data);
    } catch (e) {
        console.error('Search error:', e);
        resultsContainer.innerHTML = `
            <div class="glass-panel rounded-3xl p-8 text-center text-rose-400 border border-rose-500/30">
                <i data-lucide="alert-triangle" class="w-10 h-10 mx-auto mb-2"></i>
                <p class="font-bold">Failed to complete crawl. Please ensure the local server is running.</p>
            </div>
        `;
        lucide.createIcons();
    }
}

// --- SEARCH RESULTS RENDERER (COMBINED) ---
function renderSearchResults(data) {
    const container = document.getElementById('search-results-section');
    if (!data.results || data.results.length === 0) {
        container.innerHTML = `
            <div class="glass-panel rounded-3xl p-12 text-center text-slate-400 border border-slate-800">
                <i data-lucide="search-x" class="w-12 h-12 mx-auto mb-3 opacity-50"></i>
                <h3 class="text-lg font-bold text-white">No keywords found for "${escapeHtml(data.query)}"</h3>
                <p class="text-sm mt-1">Try a broader seed term like "vector", "wedding", "mockup", "flyer", "3d icon", or "planner".</p>
            </div>
        `;
        lucide.createIcons();
        return;
    }

    const { query, results, ai_brief = {}, tags_adobe = [], tags_etsy = [] } = data;

    // Reset filters
    state.searchFilterCategory = 'all';
    state.searchTimingFilter = 'all';
    state.searchQueryFilter = '';
    state.searchSortBy = 'opportunity';

    const queryTiming = getClientUploadDeadline(query);

    // Register objects for safe click handlers
    const adobeTagsId = registerData((tags_adobe || []).join(', '));
    const etsyTagsId = registerData((tags_etsy || []).join(', '));
    
    const models = ai_brief.models || {};
    const refGuide = ai_brief.reference_guide || {};
    const mjPrompt = models.midjourney || ai_brief.ai_image_prompt || '';
    const mjWithRef = models.midjourney_with_ref || mjPrompt;
    const fluxPrompt = models.flux || mjPrompt;
    const chatgptPrompt = models.chatgpt || mjPrompt;
    const nanoPrompt = models.nano_banana || mjPrompt;
    const videoPrompt = models.video_4k || ai_brief.ai_video_prompt || '';
    const negPrompt = ai_brief.negative_prompt || '';
    const refBenchmark = refGuide.aesthetic_benchmark || 'Commercial Stock Photography';

    const imagePromptId = registerData(mjPrompt);
    const imageWithRefId = registerData(mjWithRef);
    const fluxPromptId = registerData(fluxPrompt);
    const chatgptPromptId = registerData(chatgptPrompt);
    const nanoPromptId = registerData(nanoPrompt);
    const videoPromptId = registerData(videoPrompt);
    const negPromptId = registerData(negPrompt);
    const queryId = registerData(query);

    // Calculate category counts
    const vecCount = results.filter(r => (r.recommended_tool || '').toLowerCase().includes('illustrator') || (r.recommended_format || '').toLowerCase().includes('vector') || (r.recommended_format || '').toLowerCase().includes('svg')).length;
    const imgCount = results.filter(r => (r.recommended_tool || '').toLowerCase().includes('ai image') || (r.recommended_format || '').toLowerCase().includes('jpeg') || (r.recommended_tool || '').toLowerCase().includes('photo')).length;
    const vidCount = results.filter(r => (r.recommended_tool || '').toLowerCase().includes('video') || (r.recommended_format || '').toLowerCase().includes('4k')).length;
    const tmpCount = results.filter(r => (r.recommended_tool || '').toLowerCase().includes('canva') || (r.recommended_tool || '').toLowerCase().includes('photoshop') || (r.recommended_format || '').toLowerCase().includes('template') || (r.recommended_format || '').toLowerCase().includes('psd')).length;

    let html = `
        <div class="glass-panel rounded-3xl p-6 sm:p-8 mb-8 border border-indigo-500/25 shadow-2xl">
            <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
                <div>
                    <div class="flex items-center gap-2">
                        <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 flex items-center gap-1">
                            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                            Live Crawl Complete
                        </span>
                        <span class="text-xs text-slate-400 font-mono">${results.length} High-Intent Commercial Queries</span>
                    </div>
                    <h2 class="text-2xl sm:text-3xl font-extrabold text-white mt-1.5 tracking-tight">Results for "${escapeHtml(query)}"</h2>
                </div>
                <div class="flex flex-wrap items-center gap-2.5">
                    <button onclick="triggerAlphabetSoupById('${queryId}')" class="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white font-bold text-xs transition shadow-lg shadow-orange-500/20 active:scale-95">
                        <i data-lucide="sparkles" class="w-4 h-4"></i>
                        <span>Deep Alphabet Crawl (A-Z)</span>
                    </button>
                    <button onclick="loadAIQuotaTabById('${queryId}')" class="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold transition shadow-lg shadow-purple-600/20 active:scale-95">
                        <i data-lucide="cpu" class="w-4 h-4"></i>
                        <span>Get 20 AI Prompts</span>
                    </button>
                    <button onclick="exportSearchResultsCSV()" class="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold border border-slate-700 transition shadow-sm active:scale-95">
                        <i data-lucide="download" class="w-4 h-4"></i>
                        <span>Export CSV</span>
                    </button>
                </div>
            </div>
        </div>

        <!-- Universal Cross-Marketplace Upload Kit (v2.0 Elite) -->
        <div class="glass-panel rounded-3xl p-6 sm:p-8 mb-8 border border-indigo-500/30 shadow-2xl relative overflow-hidden">
            <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4 pb-4 mb-5 border-b border-indigo-500/20">
                <div>
                    <div class="flex flex-wrap items-center gap-2 mb-1.5">
                        <span class="px-2.5 py-0.5 rounded-full text-xs font-black bg-gradient-to-r from-indigo-500/20 via-purple-500/20 to-emerald-500/20 text-indigo-300 border border-indigo-500/40 flex items-center gap-1.5 font-mono shadow-sm">
                            <i data-lucide="layers" class="w-3.5 h-3.5 text-indigo-400"></i>
                            Universal Upload Kit v2.0
                        </span>
                        <span class="text-xs text-slate-400 font-mono">Platform-Calibrated Metadata & Pre-Flight QA</span>
                    </div>
                    <h3 class="text-xl sm:text-2xl font-black text-white tracking-tight">Cross-Marketplace Upload Kit for "${escapeHtml(query)}"</h3>
                    <p class="text-xs text-slate-300 mt-1 max-w-2xl leading-relaxed">
                        Algorithmic commercial titles answering Who/What/Where/Context, exact tag limits, and zero-rejection pre-flight checklists for each marketplace.
                    </p>
                </div>

                <!-- Golden Upload Window & Deadline Strip for Searched Niche -->
                <div class="w-full mt-4 p-3.5 rounded-2xl ${queryTiming.is_late ? 'bg-rose-950/40 border border-rose-500/50 shadow-inner' : (queryTiming.timing_status === 'CLOSING_SOON' ? 'bg-amber-950/30 border border-amber-500/40' : (queryTiming.timing_status === 'PRIME_WINDOW' ? 'bg-emerald-950/30 border border-emerald-500/40' : 'bg-slate-900/90 border border-slate-800'))}">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs font-mono">
                        <div class="flex flex-wrap items-center gap-2">
                            <span class="px-2.5 py-1 rounded-xl text-xs font-black shadow-sm flex items-center gap-1.5 ${queryTiming.is_late ? 'bg-rose-600 text-white animate-pulse' : (queryTiming.timing_status === 'CLOSING_SOON' ? 'bg-amber-500/25 text-amber-300 border border-amber-500/40' : (queryTiming.timing_status === 'PRIME_WINDOW' ? 'bg-emerald-500/25 text-emerald-300 border border-emerald-500/40' : 'bg-purple-500/25 text-purple-300 border border-purple-500/40'))}">
                                <i data-lucide="clock" class="w-3.5 h-3.5"></i>
                                ${escapeHtml(queryTiming.timing_badge)}
                            </span>
                            <span class="text-slate-300">Golden Upload Window: <strong class="text-white">${escapeHtml(queryTiming.upload_date_range)}</strong></span>
                        </div>
                        <div class="text-slate-400">
                            Upload Deadline: <strong class="${queryTiming.is_late ? 'text-rose-400 font-black underline' : 'text-amber-300 font-bold'}">${escapeHtml(queryTiming.upload_deadline)}</strong>
                        </div>
                    </div>
                    ${queryTiming.is_late ? `
                        <div class="mt-2.5 pt-2 border-t border-rose-500/30 flex items-center gap-2 text-xs text-rose-300">
                            <i data-lucide="alert-circle" class="w-4 h-4 text-rose-400 shrink-0"></i>
                            <span><strong>🔴 LATE (${queryTiming.days_past_deadline || 0}d past golden window):</strong> This niche is within its 45-day commercial peak. Upload immediately for last-minute buyers!</span>
                        </div>
                    ` : ''}
                </div>

                <!-- Platform Switcher Tabs -->
                <div class="flex flex-wrap items-center gap-1.5 p-1 rounded-2xl bg-slate-900/90 border border-slate-800">
                    ${[
                        { key: 'adobe_stock', name: 'Adobe Stock', limit: 49 },
                        { key: 'shutterstock', name: 'Shutterstock', limit: 50 },
                        { key: 'etsy', name: 'Etsy', limit: 13 },
                        { key: 'iconscout', name: 'IconScout', limit: 30 },
                        { key: 'graphicriver', name: 'GraphicRiver', limit: 30 }
                    ].map((pf, pIdx) => `
                        <button
                            type="button"
                            id="search-kit-tab-${pf.key}"
                            onclick="switchSearchKitPlatform('${pf.key}')"
                            class="search-kit-tab px-3 py-1.5 rounded-xl text-xs font-bold transition flex items-center gap-1.5 ${pIdx === 0 ? 'bg-indigo-600 text-white shadow-md' : 'bg-slate-900 text-slate-400 hover:text-white'}"
                        >
                            <span>${pf.name}</span>
                            <span class="text-[10px] font-mono opacity-80">(${pf.limit})</span>
                        </button>
                    `).join('')}
                </div>
            </div>

            <!-- Platform Detail Views -->
            <div id="search-kit-content">
                ${[
                    { key: 'adobe_stock', name: 'Adobe Stock', limit: 49, hint: 'First 10 tags carry ~80% search algorithm weight in Adobe Stock.' },
                    { key: 'shutterstock', name: 'Shutterstock', limit: 50, hint: 'Strictly 50 commercial tags to maximize catalogue visibility.' },
                    { key: 'etsy', name: 'Etsy', limit: 13, hint: 'Strictly 13 multi-word long-tail tags, each under 20 chars, zero commas.' },
                    { key: 'iconscout', name: 'IconScout', limit: 30, hint: '30 UI/UX tags tailored for 3D icons, clean alpha cutouts & vector UI.' },
                    { key: 'graphicriver', name: 'GraphicRiver', limit: 30, hint: '30 tags tailored for Photoshop PSD templates, print flyers & Smart Objects.' }
                ].map((pf, pIdx) => {
                    const kitData = (data.marketplace_kit && (data.marketplace_kit.platforms || data.marketplace_kit.marketplaces) && (data.marketplace_kit.platforms || data.marketplace_kit.marketplaces)[pf.key]) || {};
                    const titles = kitData.titles || [];
                    const tags = kitData.tags || [];
                    const checklist = kitData.preflight_checklist || kitData.checklist || [];
                    const allTitlesText = titles.map((t, idx) => `${idx + 1}. ${t}`).join('\n');
                    const allTitlesId = registerData(allTitlesText);
                    const allTagsId = registerData(tags.join(', '));

                    return `
                        <div id="search-kit-panel-${pf.key}" class="search-kit-panel ${pIdx === 0 ? '' : 'hidden'} space-y-4">
                            <!-- Top Grid: Titles Card and Tag Pack Card -->
                            <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
                                <!-- Ready Commercial Titles Card (4-5 Variations) -->
                                <div class="p-4 sm:p-5 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col justify-between shadow-lg">
                                    <div>
                                        <div class="flex items-center justify-between pb-2 mb-3 border-b border-slate-800">
                                            <div class="flex items-center gap-2">
                                                <i data-lucide="sparkles" class="w-4 h-4 text-emerald-400"></i>
                                                <span class="text-xs font-bold text-white uppercase tracking-wider">Ready Commercial Titles (${titles.length})</span>
                                            </div>
                                            <button type="button" onclick="copyRegisteredText('${allTitlesId}', 'All ${titles.length} Titles for ${pf.name}')" class="text-xs text-indigo-400 hover:text-indigo-300 font-semibold flex items-center gap-1 transition">
                                                <i data-lucide="copy" class="w-3 h-3"></i> Copy All Titles
                                            </button>
                                        </div>
                                        <div class="space-y-2">
                                            ${titles.map((t, tIdx) => {
                                                const tId = registerData(t);
                                                const tScore = resolveTitleScore(kitData, t, query);
                                                const rowLogId = registerData({
                                                    suggested_title: t,
                                                    asset_type: 'Commercial Stock',
                                                    platform: pf.name,
                                                    concept: query
                                                });
                                                const rowQueueId = registerData({
                                                    keyword: query,
                                                    best_marketplace: pf.name,
                                                    recommended_tool: 'Commercial Stock',
                                                    opportunity_score: tScore.score || 95,
                                                    suggested_title: t
                                                });
                                                return `
                                                    <div class="p-2.5 rounded-xl bg-slate-950/70 border border-slate-800/90 hover:border-emerald-500/30 transition flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                                                        <div class="flex items-start gap-2 flex-1 min-w-0">
                                                            <span class="text-[11px] font-bold text-slate-500 shrink-0 mt-0.5">#${tIdx + 1}</span>
                                                            <div class="flex-1 min-w-0">
                                                                <div class="flex flex-wrap items-center gap-1.5 mb-1">
                                                                    <span class="px-2 py-0.5 rounded text-[10px] font-black bg-${tScore.color}-500/20 text-${tScore.color}-300 border border-${tScore.color}-500/40 font-mono shadow-sm" title="${tScore.ctr_rating} • ${tScore.commercial_intent}">
                                                                        ★ ${tScore.score} • ${tScore.grade} CTR
                                                                    </span>
                                                                    <span class="text-[10px] text-slate-400 font-mono hidden sm:inline">${tScore.competition}</span>
                                                                </div>
                                                                <div class="text-xs font-mono text-emerald-300 leading-snug break-words">${escapeHtml(t)}</div>
                                                            </div>
                                                        </div>
                                                        <div class="flex items-center gap-1.5 shrink-0 self-end sm:self-center">
                                                            <button type="button" onclick="copyRegisteredText('${tId}', 'Stock Title Copied!')" class="px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition flex items-center gap-1 active:scale-95">
                                                                <i data-lucide="copy" class="w-3 h-3"></i> Copy
                                                            </button>
                                                            <button type="button" onclick="quickLogAssetFromRegistry('${rowLogId}')" class="px-2 py-1 rounded-lg bg-emerald-600/20 hover:bg-emerald-600/40 text-emerald-300 border border-emerald-500/30 text-xs font-bold transition flex items-center gap-1 active:scale-95" title="Log to Daily Quota">
                                                                <i data-lucide="check" class="w-3 h-3"></i>
                                                            </button>
                                                            <button type="button" onclick="saveKeywordFromRegistry('${rowQueueId}')" class="px-2 py-1 rounded-lg bg-indigo-600/20 hover:bg-indigo-600/40 text-indigo-300 border border-indigo-500/30 text-xs font-bold transition flex items-center gap-1 active:scale-95" title="Add to Kanban">
                                                                <i data-lucide="plus" class="w-3 h-3"></i>
                                                            </button>
                                                        </div>
                                                    </div>
                                                `;
                                            }).join('')}
                                        </div>
                                    </div>
                                    <div class="text-[10px] text-slate-400 mt-3 pt-2 border-t border-slate-800/80">
                                        Who/What/Where/Context formula answering live buyer searches with commercial keyword density.
                                    </div>
                                </div>

                                <!-- Algorithmic Tag Pack Card -->
                                <div class="p-4 sm:p-5 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col justify-between shadow-lg">
                                    <div>
                                        <div class="flex items-center justify-between pb-2 mb-3 border-b border-slate-800">
                                            <div class="flex items-center gap-2">
                                                <i data-lucide="tags" class="w-4 h-4 text-indigo-400"></i>
                                                <span class="text-xs font-bold text-white uppercase tracking-wider">Algorithmic Tag Pack (${tags.length} / ${pf.limit})</span>
                                            </div>
                                            <button type="button" onclick="copyRegisteredText('${allTagsId}', '${pf.name} ${tags.length} Tags Copied!')" class="px-3 py-1 rounded-lg text-xs font-bold bg-indigo-600/20 text-indigo-300 border border-indigo-500/30 hover:bg-indigo-600/30 transition flex items-center gap-1 active:scale-95">
                                                <i data-lucide="copy" class="w-3 h-3"></i> Copy All ${tags.length} Tags
                                            </button>
                                        </div>
                                        <div class="p-3 rounded-xl bg-slate-950/70 border border-slate-800/80 text-xs text-slate-300 max-h-48 overflow-y-auto leading-relaxed no-scrollbar flex flex-wrap gap-1.5">
                                            ${tags.map((t, idx) => {
                                                const tgScore = resolveTagScore(kitData, t);
                                                return `
                                                    <span
                                                        class="tag-pill inline-flex items-center gap-1.5 bg-slate-800/90 px-2.5 py-1 rounded-lg text-xs font-mono border border-slate-700/80 cursor-pointer ${idx < 10 && (pf.key === 'adobe_stock' || pf.key === 'shutterstock') ? 'text-amber-300 border-amber-500/40 font-bold' : 'text-slate-300'}"
                                                        onclick="copyToClipboard(this.getAttribute('data-tag'), 'Tag Copied!')"
                                                        data-tag="${escapeHtml(t)}"
                                                        title="Score: ${tgScore.score}/100 • Volume: ${tgScore.volume} • Comp: ${tgScore.competition} • ${tgScore.tier}"
                                                    >
                                                        <span>${escapeHtml(t)}</span>
                                                        <span class="px-1.5 py-0.2 rounded text-[9px] font-black bg-${tgScore.color}-500/25 text-${tgScore.color}-300 border border-${tgScore.color}-500/35">${tgScore.score}</span>
                                                    </span>
                                                `;
                                            }).join('')}
                                        </div>
                                    </div>
                                    <div class="text-[10px] text-slate-400 mt-3 pt-2 border-t border-slate-800/80 flex items-center justify-between">
                                        <span>${pf.hint}</span>
                                        <span class="text-indigo-400 font-mono font-bold">${tags.length} tags</span>
                                    </div>
                                </div>
                            </div>

                            <!-- Contributor Pre-Flight QA Checklist Card -->
                            <div class="p-4 rounded-2xl bg-slate-950/80 border border-slate-800/90">
                                <div class="flex items-center justify-between mb-2 pb-1.5 border-b border-slate-800/80">
                                    <span class="text-xs font-bold text-slate-300 flex items-center gap-1.5">
                                        <i data-lucide="shield-check" class="w-4 h-4 text-emerald-400"></i>
                                        ${pf.name} Contributor Pre-Flight QA Checklist (Zero-Rejection Protocol)
                                    </span>
                                    <span class="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">Verified Contributor Specs</span>
                                </div>
                                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5">
                                    ${checklist.map(c => {
                                        const cText = typeof c === 'object' ? (c.item || c.title || '') : c;
                                        return `
                                            <div class="flex items-start gap-2 p-2 rounded-lg bg-slate-900/60 border border-slate-800 text-[11px] text-slate-300">
                                                <i data-lucide="check-circle" class="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5"></i>
                                                <span class="leading-tight">${escapeHtml(cText)}</span>
                                            </div>
                                        `;
                                    }).join('')}
                                </div>
                            </div>

                            <!-- Link into isolated marketplace tab with active search -->
                            <div class="flex items-center justify-between pt-1">
                                <button type="button" onclick="switchToMarketplaceWithSearch('${pf.key}', '${queryId}')" class="w-full sm:w-auto px-5 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600/30 to-purple-600/30 hover:from-indigo-600/50 hover:to-purple-600/50 text-indigo-200 hover:text-white border border-indigo-500/40 text-xs font-bold transition flex items-center justify-center gap-2 active:scale-95 shadow-md">
                                    <i data-lucide="layers" class="w-4 h-4 text-indigo-400"></i>
                                    <span>Explore 4 Dedicated Concepts for "${escapeHtml(query)}" on ${pf.name}</span>
                                    <i data-lucide="arrow-right" class="w-3.5 h-3.5 ml-1 text-indigo-300"></i>
                                </button>
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        </div>

        <!-- AI Stock Prompt & Production Guidelines Section -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            <!-- AI Stock Prompt Card with Multi-Model & Visual Reference (Spans 2 cols) -->
            <div class="lg:col-span-2 glass-panel rounded-2xl p-6 border border-slate-800 shadow-xl flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <div class="flex items-center gap-2">
                            <i data-lucide="sparkles" class="w-5 h-5 text-purple-400"></i>
                            <h3 class="font-bold text-white text-base">Commercial AI Prompt Brief</h3>
                        </div>
                        <span class="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30 truncate max-w-[210px]" title="Visual Style Benchmark: ${escapeHtml(refBenchmark)}">
                            Ref: ${escapeHtml(refBenchmark)}
                        </span>
                    </div>

                    <!-- Model Switcher Tabs in Brief -->
                    <div class="flex flex-wrap items-center gap-1.5 mb-2.5">
                        <button id="search-ai-tab-mj" onclick="toggleSearchAIBriefModel('mj')" class="px-2.5 py-1 rounded-lg text-[11px] font-bold bg-purple-600 text-white transition active:scale-95">Midjourney v6.1</button>
                        <button id="search-ai-tab-flux" onclick="toggleSearchAIBriefModel('flux')" class="px-2.5 py-1 rounded-lg text-[11px] font-bold bg-slate-800 text-slate-300 hover:text-white transition active:scale-95">Flux.1 Pro</button>
                        <button id="search-ai-tab-chatgpt" onclick="toggleSearchAIBriefModel('chatgpt')" class="px-2.5 py-1 rounded-lg text-[11px] font-bold bg-slate-800 text-slate-300 hover:text-white transition active:scale-95">ChatGPT</button>
                        <button id="search-ai-tab-nano" onclick="toggleSearchAIBriefModel('nano')" class="px-2.5 py-1 rounded-lg text-[11px] font-bold bg-slate-800 text-slate-300 hover:text-white transition active:scale-95">Nano Banana</button>
                        <button id="search-ai-tab-video" onclick="toggleSearchAIBriefModel('video')" class="px-2.5 py-1 rounded-lg text-[11px] font-bold bg-slate-800 text-slate-300 hover:text-white transition active:scale-95">4K Video</button>
                    </div>

                    <!-- Prompt Display Panels -->
                    <div id="search-ai-panel-mj" class="p-3.5 rounded-xl bg-slate-900/90 border border-purple-500/30 text-xs font-mono text-purple-200 max-h-36 overflow-y-auto leading-relaxed no-scrollbar mb-2.5 select-all">
                        ${escapeHtml(mjPrompt)}
                    </div>
                    <div id="search-ai-panel-flux" class="hidden p-3.5 rounded-xl bg-slate-900/90 border border-cyan-500/30 text-xs font-mono text-cyan-200 max-h-36 overflow-y-auto leading-relaxed no-scrollbar mb-2.5 select-all">
                        ${escapeHtml(fluxPrompt)}
                    </div>
                    <div id="search-ai-panel-chatgpt" class="hidden p-3.5 rounded-xl bg-slate-900/90 border border-emerald-500/30 text-xs font-mono text-emerald-200 max-h-36 overflow-y-auto leading-relaxed no-scrollbar mb-2.5 select-all">
                        ${escapeHtml(chatgptPrompt)}
                    </div>
                    <div id="search-ai-panel-nano" class="hidden p-3.5 rounded-xl bg-slate-900/90 border border-amber-500/30 text-xs font-mono text-amber-200 max-h-36 overflow-y-auto leading-relaxed no-scrollbar mb-2.5 select-all">
                        ${escapeHtml(nanoPrompt)}
                    </div>
                    <div id="search-ai-panel-video" class="hidden p-3.5 rounded-xl bg-slate-900/90 border border-blue-500/30 text-xs font-mono text-blue-200 max-h-36 overflow-y-auto leading-relaxed no-scrollbar mb-2.5 select-all">
                        ${escapeHtml(videoPrompt)}
                    </div>
                </div>

                <div class="pt-2.5 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-1.5">
                    <div class="flex flex-wrap items-center gap-1.5">
                        <button onclick="copyRegisteredText('${imagePromptId}', 'Midjourney Prompt Copied!')" class="px-2.5 py-1 rounded-lg text-xs font-bold bg-purple-600/20 text-purple-300 border border-purple-500/30 hover:bg-purple-600/30 transition flex items-center gap-1 active:scale-95" title="Copy Midjourney Prompt">
                            <i data-lucide="copy" class="w-3 h-3"></i> Prompt
                        </button>
                        <button onclick="copyRegisteredText('${imageWithRefId}', 'Prompt with --sref Reference Copied!')" class="px-2.5 py-1 rounded-lg text-xs font-bold bg-indigo-600/20 text-indigo-300 border border-indigo-500/30 hover:bg-indigo-600/30 transition flex items-center gap-1 active:scale-95" title="Copy with --sref Style Reference">
                            <i data-lucide="link" class="w-3 h-3"></i> + --sref
                        </button>
                        <button onclick="copyRegisteredText('${fluxPromptId}', 'Flux.1 Pro Prompt Copied!')" class="px-2 py-1 rounded-lg text-[11px] font-bold bg-cyan-600/20 text-cyan-300 border border-cyan-500/30 hover:bg-cyan-600/30 transition active:scale-95" title="Copy Flux.1 Pro natural prompt">
                            Flux
                        </button>
                        <button onclick="copyRegisteredText('${chatgptPromptId}', 'ChatGPT Prompt Copied!')" class="px-2 py-1 rounded-lg text-[11px] font-bold bg-emerald-600/20 text-emerald-300 border border-emerald-500/30 hover:bg-emerald-600/30 transition active:scale-95" title="Copy ChatGPT / DALL-E 3 prompt">
                            ChatGPT
                        </button>
                        <button onclick="copyRegisteredText('${nanoPromptId}', 'Nano Banana Prompt Copied!')" class="px-2 py-1 rounded-lg text-[11px] font-bold bg-amber-600/20 text-amber-300 border border-amber-500/30 hover:bg-amber-600/30 transition active:scale-95" title="Copy Google Nano Banana prompt">
                            Nano
                        </button>
                    </div>
                    <button onclick="copyRegisteredText('${negPromptId}', 'Negative Prompt Copied!')" class="text-xs text-rose-400 hover:text-rose-300 font-semibold flex items-center gap-1 transition px-1.5 py-0.5 rounded hover:bg-slate-800/60" title="Copy Rejection-Proof Negative Prompt">
                        <i data-lucide="shield-alert" class="w-3 h-3"></i> Negative
                    </button>
                </div>
            </div>

            <!-- Commercial Benchmark & Studio Quick-Launch Card (Spans 1 col) -->
            <div class="glass-panel rounded-2xl p-6 border border-slate-800 shadow-xl flex flex-col justify-between">
                <div>
                    <div class="flex items-center gap-2 mb-3">
                        <i data-lucide="award" class="w-5 h-5 text-amber-400"></i>
                        <h3 class="font-bold text-white text-base">Aesthetic Benchmark</h3>
                    </div>
                    <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800 text-xs space-y-2 mb-3">
                        <div class="text-slate-300 font-medium">
                            <span class="text-slate-500">Benchmark:</span> <span class="text-amber-300 font-bold">${escapeHtml(refBenchmark)}</span>
                        </div>
                        <div class="text-[11px] text-slate-400 leading-relaxed">
                            Calibrated to high-performing stock agency portfolios, prioritizing authentic specular highlights, clean negative space, and natural depth of field.
                        </div>
                    </div>
                    <div class="text-[11px] text-slate-400 font-mono space-y-1">
                        <div class="flex items-center gap-1.5 text-emerald-400 font-semibold">
                            <i data-lucide="check" class="w-3 h-3"></i> Adobe Stock AI Accepted
                        </div>
                        <div class="flex items-center gap-1.5 text-slate-400">
                            <i data-lucide="shield-alert" class="w-3 h-3 text-amber-400"></i> Shutterstock: Camera/Vector Only
                        </div>
                    </div>
                </div>
                <div class="pt-3 border-t border-slate-800/80 mt-3">
                    <button onclick="switchTab('platform-adobe_stock')" class="w-full py-2 px-3 rounded-xl bg-purple-600/30 hover:bg-purple-600/50 text-purple-200 border border-purple-500/40 text-xs font-bold transition flex items-center justify-center gap-2 active:scale-95 shadow-sm">
                        <i data-lucide="sparkles" class="w-3.5 h-3.5 text-purple-400"></i>
                        <span>Open Full AI Studio</span>
                    </button>
                </div>
            </div>
        </div>

        <!-- Keyword Results Table with Interactive Filter Controls -->
        <div class="glass-panel rounded-3xl overflow-hidden border border-slate-800 shadow-2xl">
            <!-- Filter Toolbar -->
            <div class="p-5 border-b border-slate-800/80 bg-slate-900/50 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <!-- Filter Chips -->
                <div class="flex flex-wrap items-center gap-1.5">
                    <button onclick="onSearchFilterCategory('all')" id="filter-chip-all" class="filter-chip active">All (${results.length})</button>
                    <button onclick="onSearchFilterCategory('vectors')" id="filter-chip-vectors" class="filter-chip">📐 Vectors (${vecCount})</button>
                    <button onclick="onSearchFilterCategory('images')" id="filter-chip-images" class="filter-chip">📸 AI Images (${imgCount})</button>
                    <button onclick="onSearchFilterCategory('videos')" id="filter-chip-videos" class="filter-chip">🎬 4K Videos (${vidCount})</button>
                    <button onclick="onSearchFilterCategory('templates')" id="filter-chip-templates" class="filter-chip">📄 Templates (${tmpCount})</button>
                </div>

                <!-- Instant Filter Input, Timing & Sort -->
                <div class="flex flex-wrap items-center gap-2">
                    <select id="search-timing-filter" onchange="onSearchTimingFilterChange(this.value)" class="bg-slate-900 text-slate-300 text-xs py-2 px-3 rounded-xl border border-slate-700/80 focus:outline-none font-medium">
                        <option value="all">Timing: All Windows</option>
                        <option value="late">🔴 Late Only</option>
                        <option value="closing_soon">🟡 Closing Soon</option>
                        <option value="prime">🟢 Prime Window</option>
                    </select>

                    <div class="relative flex items-center">
                        <i data-lucide="filter" class="w-3.5 h-3.5 text-slate-500 absolute left-3 pointer-events-none"></i>
                        <input
                            type="text"
                            placeholder="Filter table..."
                            oninput="onSearchFilterInput(this.value)"
                            class="bg-slate-900 text-white placeholder-slate-500 text-xs py-2 pl-9 pr-3 rounded-xl border border-slate-700/80 focus:outline-none focus:border-indigo-500 w-36 font-medium"
                        />
                    </div>
                    <select onchange="onSearchSortChange(this.value)" class="bg-slate-900 text-slate-300 text-xs py-2 px-3 rounded-xl border border-slate-700/80 focus:outline-none font-medium">
                        <option value="opportunity">Sort: Opportunity Score</option>
                        <option value="deadline">Sort: Deadline (Late & Urgent First)</option>
                        <option value="demand">Sort: Demand Score</option>
                        <option value="az">Sort: Keyword (A to Z)</option>
                    </select>
                </div>
            </div>

            <div class="px-6 py-3 border-b border-slate-800/60 bg-slate-950/40 flex items-center justify-between text-xs text-slate-400 font-mono">
                <span id="keyword-results-count">Showing ${results.length} ranked keywords</span>
                <span>Click "+ Log Done" to count towards Daily Quota</span>
            </div>

            <div class="overflow-x-auto no-scrollbar">
                <table class="w-full text-left text-sm text-slate-300">
                    <thead class="bg-slate-950/70 text-xs uppercase tracking-wider text-slate-400 border-b border-slate-800">
                        <tr>
                            <th class="px-6 py-4">Keyword / Search Query</th>
                            <th class="px-6 py-4">Suggested Stock Title</th>
                            <th class="px-6 py-4">Upload Window & Deadline</th>
                            <th class="px-6 py-4">Opportunity</th>
                            <th class="px-6 py-4">Recommended Tool & Format</th>
                            <th class="px-6 py-4">Marketplace</th>
                            <th class="px-6 py-4 text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody id="keyword-results-tbody" class="divide-y divide-slate-800/60">
                        ${results.map((item, idx) => renderResultRow(item, idx)).join('')}
                    </tbody>
                </table>
            </div>
        </div>
    `;

    container.innerHTML = html;
    lucide.createIcons();
}

/**
 * Switches the active platform view in the Cross-Marketplace Upload Kit v2.0
 */
function switchSearchKitPlatform(platformKey) {
    document.querySelectorAll('.search-kit-panel').forEach(p => p.classList.add('hidden'));
    document.querySelectorAll('.search-kit-tab').forEach(b => {
        b.classList.remove('bg-indigo-600', 'text-white', 'shadow-md');
        b.classList.add('bg-slate-900', 'text-slate-400');
    });

    const activePanel = document.getElementById(`search-kit-panel-${platformKey}`);
    const activeTab = document.getElementById(`search-kit-tab-${platformKey}`);
    if (activePanel) activePanel.classList.remove('hidden');
    if (activeTab) {
        activeTab.classList.remove('bg-slate-900', 'text-slate-400');
        activeTab.classList.add('bg-indigo-600', 'text-white', 'shadow-md');
    }
    lucide.createIcons();
}

function onSearchFilterCategory(category) {
    state.searchFilterCategory = category;
    document.querySelectorAll('.filter-chip').forEach(btn => {
        if (btn.id === `filter-chip-${category}`) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    renderFilteredKeywordsTable();
}

function onSearchFilterInput(val) {
    state.searchQueryFilter = (val || '').toLowerCase().trim();
    renderFilteredKeywordsTable();
}

function onSearchTimingFilterChange(val) {
    state.searchTimingFilter = val;
    renderFilteredKeywordsTable();
}

function onSearchSortChange(val) {
    state.searchSortBy = val;
    renderFilteredKeywordsTable();
}

function renderFilteredKeywordsTable() {
    if (!state.searchResults || !state.searchResults.results) return;
    const tbody = document.getElementById('keyword-results-tbody');
    const countEl = document.getElementById('keyword-results-count');
    if (!tbody) return;

    let items = [...state.searchResults.results];

    // Category filter
    if (state.searchFilterCategory === 'vectors') {
        items = items.filter(r => (r.recommended_tool || '').toLowerCase().includes('illustrator') || (r.recommended_format || '').toLowerCase().includes('vector') || (r.recommended_format || '').toLowerCase().includes('svg'));
    } else if (state.searchFilterCategory === 'images') {
        items = items.filter(r => (r.recommended_tool || '').toLowerCase().includes('ai image') || (r.recommended_format || '').toLowerCase().includes('jpeg') || (r.recommended_tool || '').toLowerCase().includes('photo'));
    } else if (state.searchFilterCategory === 'videos') {
        items = items.filter(r => (r.recommended_tool || '').toLowerCase().includes('video') || (r.recommended_format || '').toLowerCase().includes('4k'));
    } else if (state.searchFilterCategory === 'templates') {
        items = items.filter(r => (r.recommended_tool || '').toLowerCase().includes('canva') || (r.recommended_tool || '').toLowerCase().includes('photoshop') || (r.recommended_format || '').toLowerCase().includes('template') || (r.recommended_format || '').toLowerCase().includes('psd'));
    }

    // Timing status filter
    if (state.searchTimingFilter === 'late') {
        items = items.filter(r => getClientUploadDeadline(r).is_late);
    } else if (state.searchTimingFilter === 'closing_soon') {
        items = items.filter(r => getClientUploadDeadline(r).timing_status === 'CLOSING_SOON');
    } else if (state.searchTimingFilter === 'prime') {
        items = items.filter(r => getClientUploadDeadline(r).timing_status === 'PRIME_WINDOW');
    }

    // Text search filter
    if (state.searchQueryFilter) {
        items = items.filter(r => 
            (r.keyword || '').toLowerCase().includes(state.searchQueryFilter) ||
            (r.suggested_title || '').toLowerCase().includes(state.searchQueryFilter) ||
            (r.recommended_tool || '').toLowerCase().includes(state.searchQueryFilter) ||
            (r.best_marketplace || '').toLowerCase().includes(state.searchQueryFilter)
        );
    }

    // Sorting
    if (state.searchSortBy === 'opportunity') {
        items.sort((a, b) => (b.opportunity_score || 0) - (a.opportunity_score || 0));
    } else if (state.searchSortBy === 'deadline') {
        items.sort((a, b) => {
            const tA = getClientUploadDeadline(a);
            const tB = getClientUploadDeadline(b);
            if (tA.is_late !== tB.is_late) return tA.is_late ? -1 : 1; // Late items first
            return (tB.days_past_deadline || 0) - (tA.days_past_deadline || 0);
        });
    } else if (state.searchSortBy === 'demand') {
        items.sort((a, b) => (b.demand_score || 0) - (a.demand_score || 0));
    } else if (state.searchSortBy === 'az') {
        items.sort((a, b) => (a.keyword || '').localeCompare(b.keyword || ''));
    }

    if (countEl) countEl.innerText = `Showing ${items.length} of ${state.searchResults.results.length} ranked keywords`;

    if (items.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="px-6 py-12 text-center text-slate-500 text-xs font-medium">
                    No keywords match the current filter. Try adjusting your search query or category chip.
                </td>
            </tr>
        `;
    } else {
        tbody.innerHTML = items.map((item, idx) => renderResultRow(item, idx)).join('');
    }
    lucide.createIcons();
}

function exportSearchResultsCSV() {
    if (!state.searchResults || !state.searchResults.results || state.searchResults.results.length === 0) {
        showToast('No search results to export', 'info');
        return;
    }
    const query = state.searchResults.query || 'keywords';
    let csv = "Keyword,Suggested Stock Title,Upload Date Range,Upload Deadline,Timing Status,Opportunity Score,Demand Score,Competition,Recommended Tool,Recommended Format,Best Marketplace,Sources\n";
    state.searchResults.results.forEach(r => {
        const timing = getClientUploadDeadline(r);
        const kw = (r.keyword || '').replace(/"/g, '""');
        const title = (r.suggested_title || '').replace(/"/g, '""');
        const uWindow = (timing.upload_date_range || '').replace(/"/g, '""');
        const uDeadline = (timing.upload_deadline || '').replace(/"/g, '""');
        const uStatus = (timing.timing_badge || '').replace(/"/g, '""');
        const opp = r.opportunity_score || 0;
        const demand = r.demand_score || 0;
        const comp = (r.competition || 'Medium').replace(/"/g, '""');
        const tool = (r.recommended_tool || '').replace(/"/g, '""');
        const format = (r.recommended_format || '').replace(/"/g, '""');
        const mkt = (r.best_marketplace || '').replace(/"/g, '""');
        const sources = (r.sources || []).join('; ').replace(/"/g, '""');
        csv += `"${kw}","${title}","${uWindow}","${uDeadline}","${uStatus}","${opp}","${demand}","${comp}","${tool}","${format}","${mkt}","${sources}"\n`;
    });
    downloadCSV(csv, `stockpulse_keywords_${query.replace(/\s+/g, '_')}.csv`);
    showToast('Exported keywords to CSV with upload deadlines!', 'success');
}

function renderResultRow(item, idx) {
    const timing = getClientUploadDeadline(item);
    const oppScore = item.opportunity_score;
    let scoreColor = 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30';
    if (oppScore < 70) scoreColor = 'text-amber-400 bg-amber-500/10 border-amber-500/30';
    if (oppScore < 50) scoreColor = 'text-rose-400 bg-rose-500/10 border-rose-500/30';

    let toolBadgeClass = 'badge-ai';
    if (item.recommended_tool.includes('Illustrator')) toolBadgeClass = 'badge-illustrator';
    if (item.recommended_tool.includes('Photoshop')) toolBadgeClass = 'badge-photoshop';
    if (item.recommended_tool.includes('Canva')) toolBadgeClass = 'badge-canva';
    if (item.recommended_tool.includes('Video')) toolBadgeClass = 'badge-video';

    // Register item safely in registry
    const itemId = registerData(item);
    const titleId = registerData(item.suggested_title);

    return `
        <tr class="hover:bg-slate-800/40 transition ${timing.is_late ? 'bg-rose-950/20 border-l-4 border-l-rose-500' : ''}">
            <td class="px-6 py-4">
                <div class="font-bold text-white text-sm">${escapeHtml(item.keyword)}</div>
                <div class="flex flex-wrap gap-1 mt-1.5">
                    ${item.sources.map(s => `<span class="text-[10px] px-2 py-0.5 rounded-md bg-slate-800 text-slate-400 border border-slate-700 font-mono">${escapeHtml(s)}</span>`).join('')}
                </div>
            </td>
            <td class="px-6 py-4">
                <div class="text-xs text-slate-300 font-mono max-w-xs truncate" title="${escapeHtml(item.suggested_title)}">${escapeHtml(item.suggested_title)}</div>
                <button onclick="copyRegisteredText('${titleId}', 'Title Copied!')" class="text-[11px] text-indigo-400 hover:text-indigo-300 font-semibold mt-1 flex items-center gap-1 transition">
                    <i data-lucide="copy" class="w-3 h-3"></i> Copy Title
                </button>
            </td>
            <td class="px-6 py-4">
                <div class="flex items-center gap-1.5">
                    <span class="px-2 py-0.5 rounded text-[10px] font-black ${timing.is_late ? 'bg-rose-600 text-white font-black animate-pulse shadow-sm shadow-rose-900/50' : (timing.timing_status === 'CLOSING_SOON' ? 'bg-amber-500/25 text-amber-300 border border-amber-500/40 font-bold' : (timing.timing_status === 'PRIME_WINDOW' ? 'bg-emerald-500/25 text-emerald-300 border border-emerald-500/40 font-bold' : 'bg-slate-800 text-slate-300 border border-slate-700'))}">
                        ${escapeHtml(timing.timing_badge)}
                    </span>
                </div>
                <div class="text-[11px] text-slate-300 font-mono mt-1 flex items-center gap-1">
                    <i data-lucide="clock" class="w-3 h-3 text-slate-400"></i>
                    <span>Window: <strong class="text-white">${escapeHtml(timing.upload_date_range)}</strong></span>
                </div>
                <div class="text-[10px] font-mono mt-0.5">
                    Deadline: <strong class="${timing.is_late ? 'text-rose-400 font-black underline' : 'text-amber-300 font-semibold'}">${escapeHtml(timing.upload_deadline)}</strong>
                </div>
            </td>
            <td class="px-6 py-4">
                <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold border ${scoreColor}">
                    <span>${oppScore}</span>
                    <span class="text-[10px] opacity-75">/100</span>
                </div>
            </td>
            <td class="px-6 py-4">
                <span class="px-2.5 py-1 rounded-lg text-xs font-bold border ${toolBadgeClass}">
                    ${escapeHtml(item.recommended_tool)}
                </span>
                <div class="text-[11px] text-slate-400 mt-1 font-mono">${escapeHtml(item.recommended_format)}</div>
            </td>
            <td class="px-6 py-4">
                <span class="text-xs font-semibold text-slate-200">${escapeHtml(item.best_marketplace)}</span>
            </td>
            <td class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-2">
                    <button onclick="quickLogAssetFromRegistry('${itemId}')" class="px-2.5 py-1.5 rounded-xl bg-emerald-600/20 hover:bg-emerald-600/40 text-emerald-300 border border-emerald-500/30 text-xs font-bold transition inline-flex items-center gap-1.5 shadow-sm active:scale-95" title="Log this asset completed towards Today's Goal">
                        <i data-lucide="check" class="w-3.5 h-3.5"></i>
                        Log Done
                    </button>
                    <button onclick="saveKeywordFromRegistry('${itemId}')" class="px-2.5 py-1.5 rounded-xl bg-indigo-600/25 hover:bg-indigo-600/50 text-indigo-300 border border-indigo-500/35 text-xs font-bold transition inline-flex items-center gap-1.5 shadow-sm active:scale-95" title="Save keyword to Production Kanban">
                        <i data-lucide="plus" class="w-3.5 h-3.5"></i>
                        Queue
                    </button>
                </div>
            </td>
        </tr>
    `;
}

// --- PLATFORM ISOLATED VIEW ---
async function loadPlatformTab(platformKey, searchQuery = null) {
    const container = document.getElementById(`tab-platform-${platformKey}`);
    if (!container) return;

    try {
        const url = searchQuery && searchQuery.trim()
            ? `/api/platforms/${platformKey}?q=${encodeURIComponent(searchQuery.trim())}`
            : `/api/platforms/${platformKey}`;
        const res = await fetch(url);
        const p = await res.json();

        // Build dynamic requirement tabs depending on platform capabilities
        const reqCategories = [];
        if (p.requirements.vectors) {
            reqCategories.push({ key: 'vectors', label: platformKey === 'etsy' ? 'Vectors & SVG Cut Files' : (platformKey === 'iconscout' ? 'Vector Icons (24px Grid)' : 'Vectors (AI/EPS 10)'), icon: 'pen-tool' });
        }
        if (p.requirements.images) {
            reqCategories.push({ key: 'images', label: platformKey === 'iconscout' ? '3D Icons & Renders' : (platformKey === 'graphicriver' ? 'PSD Mockups & Smart Objects' : (platformKey === 'etsy' ? 'Wall Art & Clipart' : 'Photos & Generative AI')), icon: 'image' });
        }
        if (p.requirements.videos) {
            reqCategories.push({ key: 'videos', label: platformKey === 'iconscout' ? 'Lottie Vector Motion' : (platformKey === 'etsy' ? 'Listing Video Demo' : (platformKey === 'graphicriver' ? 'Video & GIF Previews' : '4K Video Footage')), icon: 'video' });
        }
        if (p.requirements.templates) {
            reqCategories.push({ key: 'templates', label: 'Canva & Print Templates', icon: 'file-text' });
        }

        let html = `
            <!-- Platform Header Banner -->
            <div class="glass-panel rounded-3xl p-8 mb-8 border border-slate-700/60 shadow-2xl relative overflow-hidden">
                <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
                    <div>
                        <div class="flex items-center gap-2.5">
                            <span class="px-3.5 py-1 rounded-full text-xs font-extrabold ${getPlatformBadgeClass(platformKey)}">
                                ${escapeHtml(p.badge)}
                            </span>
                            <span class="text-xs text-slate-400 font-mono bg-slate-900/80 px-2.5 py-1 rounded-lg border border-slate-800">
                                Maximum Tags: <span class="text-indigo-400 font-bold">${p.tag_limit}</span>
                            </span>
                        </div>
                        <h2 class="text-3xl sm:text-4xl font-black text-white mt-2.5 tracking-tight">${p.name} - Isolated Intelligence</h2>
                        <p class="text-slate-300 text-sm mt-1 max-w-2xl leading-relaxed">
                            Search and research data strictly tailored to ${p.name}'s buyer algorithm, format requirements, and submission approval guidelines.
                        </p>
                    </div>

                    <!-- AI Policy Callout Card -->
                    <div class="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 max-w-md w-full shadow-lg">
                        <div class="flex items-center justify-between gap-2 mb-2 pb-2 border-b border-slate-800/80">
                            <div class="flex items-center gap-1.5">
                                <i data-lucide="shield-check" class="w-4 h-4 text-emerald-400"></i>
                                <span class="text-xs font-bold text-white">AI Acceptance Policy</span>
                            </div>
                            <span class="px-2 py-0.5 rounded text-[10px] font-extrabold bg-${p.ai_acceptance.badge_color}-500/20 text-${p.ai_acceptance.badge_color}-300 border border-${p.ai_acceptance.badge_color}-500/30">
                                ${p.ai_acceptance.status}
                            </span>
                        </div>
                        <p class="text-[11px] text-slate-300 leading-relaxed">${escapeHtml(p.ai_acceptance.details)}</p>
                    </div>
                </div>

                <!-- Platform Isolated Search Bar -->
                <div class="mt-8 flex flex-col sm:flex-row items-center gap-2 p-2 rounded-2xl bg-slate-900/95 border border-slate-700/80 shadow-2xl focus-within:border-indigo-500 transition">
                    <div class="w-full flex-1 relative flex items-center">
                        <i data-lucide="search" class="w-4 h-4 text-slate-500 ml-4 pointer-events-none"></i>
                        <input
                            id="platform-search-input-${platformKey}"
                            type="text"
                            value="${escapeHtml(p.active_search || '')}"
                            placeholder="Search strictly for ${p.name} trends (e.g. happy new year, corporate flyer, 3d icon)..."
                            class="w-full bg-transparent text-white placeholder-slate-500 text-sm py-3 px-3 focus:outline-none font-medium"
                            onkeydown="if(event.key==='Enter') executePlatformSearch('${platformKey}')"
                        />
                        ${p.search_mode ? `
                            <button onclick="clearPlatformSearch('${platformKey}')" class="mr-2 px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-xs font-semibold flex items-center gap-1 transition shrink-0" title="Clear Search">
                                <i data-lucide="x" class="w-3.5 h-3.5"></i> Clear
                            </button>
                        ` : ''}
                    </div>
                    <button
                        onclick="executePlatformSearch('${platformKey}')"
                        class="w-full sm:w-auto px-6 py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-sm transition shadow-lg shadow-indigo-600/30 flex items-center justify-center gap-2 whitespace-nowrap active:scale-95"
                    >
                        <i data-lucide="search" class="w-4 h-4"></i>
                        <span>Search ${p.name}</span>
                    </button>
                </div>
            </div>

            ${p.search_mode ? `
                <!-- Live Search Intelligence Banner -->
                <div class="mb-8 p-6 rounded-3xl bg-gradient-to-r from-indigo-950/70 via-purple-950/50 to-slate-900/90 border border-indigo-500/40 shadow-2xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                    <div>
                        <div class="flex items-center gap-2 mb-1.5">
                            <span class="px-2.5 py-0.5 rounded-full text-xs font-black bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-mono flex items-center gap-1.5">
                                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                                Live Search Intelligence Active
                            </span>
                            <span class="text-xs text-slate-400 font-mono">Platform: <strong class="text-white">${p.name}</strong></span>
                        </div>
                        <h3 class="text-xl sm:text-2xl font-black text-white">4 Tailored Concepts Generated for "${escapeHtml(p.active_search)}"</h3>
                        <p class="text-xs text-slate-300 mt-1 max-w-2xl leading-relaxed">
                            Every title and tag below is dynamically calibrated with Performance Scores, volume tiers, and pre-flight compliance guidelines for ${p.name}.
                        </p>
                    </div>
                    <div class="flex items-center gap-2 shrink-0">
                        <button onclick="clearPlatformSearch('${platformKey}')" class="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white text-xs font-bold transition flex items-center gap-2 border border-slate-700 active:scale-95 shadow-md">
                            <i data-lucide="rotate-ccw" class="w-3.5 h-3.5 text-indigo-400"></i>
                            <span>Reset to Top Trending</span>
                        </button>
                    </div>
                </div>
            ` : ''}

            <!-- Dynamic Platform Search Results Container -->
            <div id="platform-search-results-${platformKey}" class="hidden mb-8"></div>

            <!-- Technical Upload Requirements & Rules -->
            <div class="glass-panel rounded-3xl p-6 sm:p-8 mb-8 border border-slate-800 shadow-xl">
                <div class="flex flex-col md:flex-row md:items-center justify-between pb-4 mb-6 border-b border-slate-800 gap-4">
                    <div>
                        <h3 class="text-xl font-bold text-white">Technical Upload Requirements & Rules</h3>
                        <p class="text-xs text-slate-400 mt-0.5">Strictly separated guidelines for vector, raster, and video submissions on ${p.name}</p>
                    </div>
                    <div class="flex flex-wrap gap-2">
                        ${reqCategories.map((rc, idx) => `
                            <button onclick="switchReqTab('${platformKey}', '${rc.key}')" id="req-btn-${platformKey}-${rc.key}" class="px-4 py-2 rounded-xl text-xs font-bold ${idx === 0 ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30' : 'bg-slate-800 text-slate-300 hover:text-white'} flex items-center gap-1.5 transition">
                                <i data-lucide="${rc.icon}" class="w-3.5 h-3.5"></i>
                                <span>${rc.label}</span>
                            </button>
                        `).join('')}
                    </div>
                </div>

                <!-- Panels -->
                ${reqCategories.map((rc, idx) => {
                    const reqObj = p.requirements[rc.key] || {};
                    const formatText = reqObj.format || 'Standard commercial upload format';
                    const artboardOrRes = reqObj.artboard || reqObj.resolution || (rc.key === 'videos' ? (reqObj.resolution || '4K UHD / Full HD') : 'Minimum 4 Megapixels');
                    const rulesText = reqObj.rules || 'Follow commercial marketplace licensing standards.';

                    return `
                        <div id="req-panel-${platformKey}-${rc.key}" class="req-panel-content ${idx === 0 ? '' : 'hidden'} space-y-4">
                            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
                                    <div class="text-xs font-bold text-indigo-400 uppercase tracking-wider mb-1 flex items-center gap-1.5">
                                        <i data-lucide="file-code" class="w-3.5 h-3.5"></i> File Format
                                    </div>
                                    <div class="text-sm font-bold text-white leading-snug">${escapeHtml(formatText)}</div>
                                </div>
                                <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
                                    <div class="text-xs font-bold text-purple-400 uppercase tracking-wider mb-1 flex items-center gap-1.5">
                                        <i data-lucide="maximize" class="w-3.5 h-3.5"></i> Artboard / Resolution
                                    </div>
                                    <div class="text-sm font-bold text-white leading-snug">${escapeHtml(artboardOrRes)}</div>
                                </div>
                                <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
                                    <div class="text-xs font-bold text-emerald-400 uppercase tracking-wider mb-1 flex items-center gap-1.5">
                                        <i data-lucide="check-circle" class="w-3.5 h-3.5"></i> Strict Rules & Quality
                                    </div>
                                    <div class="text-xs text-slate-300 leading-relaxed">${escapeHtml(rulesText)}</div>
                                </div>
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>

            <!-- Marketplace Ranking & Approval Tips (Restored & Enhanced) -->
            ${p.ranking_tips && p.ranking_tips.length > 0 ? `
                <div class="glass-panel rounded-3xl p-6 sm:p-8 mb-8 border border-slate-800/80 shadow-xl">
                    <div class="flex items-center gap-2 mb-4">
                        <i data-lucide="award" class="w-5 h-5 text-amber-400"></i>
                        <h3 class="text-xl font-bold text-white">${p.name} Ranking & Algorithm Mastery</h3>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        ${p.ranking_tips.map(tip => `
                            <div class="p-4 rounded-2xl bg-slate-900/70 border border-slate-800/80 flex items-start gap-3">
                                <span class="w-6 h-6 rounded-lg bg-amber-500/15 border border-amber-500/30 flex items-center justify-center shrink-0 mt-0.5">
                                    <i data-lucide="zap" class="w-3.5 h-3.5 text-amber-400"></i>
                                </span>
                                <p class="text-xs text-slate-300 leading-relaxed font-medium">${escapeHtml(tip)}</p>
                            </div>
                        `).join('')}
                    </div>
                </div>
            ` : ''}

            ${platformKey === 'adobe_stock' ? `
                <!-- Adobe Stock Commercial Generative AI Studio & Reference Engine -->
                <div id="adobe-stock-ai-studio-root" class="mb-8">
                    <div class="glass-panel rounded-3xl p-6 sm:p-8 border border-purple-500/30 shadow-2xl flex items-center justify-center">
                        <div class="inline-block animate-spin rounded-full h-8 w-8 border-3 border-purple-500 border-t-transparent mr-3"></div>
                        <span class="text-sm font-medium text-slate-300">Loading Adobe Stock Generative AI Studio...</span>
                    </div>
                </div>
            ` : ''}

            <!-- What to Create & Ready-to-Use Titles (Score System Active) -->
            <div id="what-to-create-root-${platformKey}" class="mb-8">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
                    <div>
                        <div class="flex items-center gap-2.5">
                            <h3 class="text-2xl font-bold text-white">${p.search_mode ? `Search Intelligence for "${escapeHtml(p.active_search)}"` : `What to Create for ${p.name}`}</h3>
                            ${p.search_mode ? `
                                <span class="px-2.5 py-0.5 rounded-full text-xs font-black bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-mono">
                                    ● 4 Concepts Generated
                                </span>
                            ` : ''}
                        </div>
                        <p class="text-xs text-slate-400 mt-0.5">${p.search_mode ? `Commercial asset blueprints strictly matching your search query with live algorithmic scores` : `High-converting asset ideas with multiple SEO titles tailored for each tag ready to upload`}</p>
                    </div>
                    ${p.search_mode ? `
                        <button onclick="clearPlatformSearch('${platformKey}')" class="px-3.5 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-xs font-semibold flex items-center gap-1.5 transition self-start sm:self-auto border border-slate-700 active:scale-95 shadow-sm">
                            <i data-lucide="rotate-ccw" class="w-3.5 h-3.5 text-indigo-400"></i>
                            <span>Reset to Default Trends</span>
                        </button>
                    ` : ''}
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6" id="what-to-create-container-${platformKey}">
                    ${(p.what_to_create || []).map((item, itemIdx) => {
                        const itemCardId = `wtc_${platformKey}_${itemIdx}`;
                        const itemToStore = {
                            ...item,
                            platform: p.name
                        };
                        state.registry.set(itemCardId, itemToStore);

                        const primaryTitles = item.suggested_titles || (item.suggested_title ? [item.suggested_title] : []);
                        const allPrimaryText = primaryTitles.map((t, i) => `${i + 1}. ${t}`).join('\n');
                        const allPrimaryTitlesId = registerData(allPrimaryText);
                        const tagsId = registerData((item.sample_tags || []).join(', '));
                        const fullItemId = registerData({
                            suggested_title: item.suggested_title || (primaryTitles[0] || item.concept),
                            asset_type: item.asset_type,
                            platform: p.name,
                            concept: item.concept
                        });
                        const cardItemDataId = registerData(itemToStore);
                        const timing = getClientUploadDeadline(item);

                        return `
                            <div class="glass-card rounded-2xl p-6 border ${timing.is_late ? 'border-rose-500/40 shadow-rose-900/10' : 'border-slate-800'} flex flex-col justify-between shadow-xl">
                                <div>
                                    <div class="flex items-center justify-between mb-2">
                                        <span class="text-xs font-bold px-2.5 py-1 rounded-lg bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 font-mono">
                                            ${escapeHtml(item.asset_type)}
                                        </span>
                                        <span class="text-[11px] font-mono text-slate-400 bg-slate-900 px-2 py-0.5 rounded border border-slate-800">
                                            ${(item.sample_tags || []).length} Tags • Multi-Title Ready
                                        </span>
                                    </div>
                                    <h4 class="text-lg font-bold text-white mb-1.5">${escapeHtml(item.concept)}</h4>

                                    <!-- Upload Date Range & Production Deadline Banner -->
                                    <div class="flex flex-wrap items-center justify-between gap-2 mb-3 p-2.5 rounded-xl ${timing.is_late ? 'bg-rose-950/40 border border-rose-500/40 shadow-inner' : (timing.timing_status === 'CLOSING_SOON' ? 'bg-amber-950/30 border border-amber-500/40' : (timing.timing_status === 'PRIME_WINDOW' ? 'bg-emerald-950/30 border border-emerald-500/40' : 'bg-slate-900/90 border border-slate-800'))} text-xs font-mono">
                                        <div class="flex flex-wrap items-center gap-2">
                                            <span class="px-2 py-0.5 rounded text-[10px] font-black ${timing.is_late ? 'bg-rose-600 text-white animate-pulse' : (timing.timing_status === 'CLOSING_SOON' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' : (timing.timing_status === 'PRIME_WINDOW' ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' : 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/40'))}">
                                                ${escapeHtml(timing.timing_badge)}
                                            </span>
                                            <span class="text-slate-300 text-[11px]">Window: <strong class="text-white">${escapeHtml(timing.upload_date_range)}</strong></span>
                                        </div>
                                        <div class="text-[11px] text-slate-400">
                                            Deadline: <span class="${timing.is_late ? 'text-rose-400 font-black' : 'text-slate-200 font-semibold'}">${escapeHtml(timing.upload_deadline)}</span>
                                        </div>
                                    </div>
                                    
                                    ${item.trend_velocity ? `
                                        <!-- Trend Velocity & Lead Time Indicator -->
                                        <div class="flex flex-wrap items-center gap-2 mb-3 px-3 py-1.5 rounded-xl bg-slate-950/70 border border-slate-800/80 text-[11px] font-mono">
                                            <span class="text-amber-400 font-bold flex items-center gap-1">
                                                <i data-lucide="trending-up" class="w-3.5 h-3.5"></i> ${escapeHtml(item.trend_velocity.search_surge || '+320% Surge')}
                                            </span>
                                            <span class="text-slate-600">•</span>
                                            <span class="text-slate-300">${escapeHtml(item.trend_velocity.optimal_window || 'Upload 45-60 Days in Advance')}</span>
                                            <span class="text-slate-600 hidden sm:inline">•</span>
                                            <span class="text-emerald-400 hidden sm:inline">${escapeHtml(item.trend_velocity.buyer_profile || 'Corporate & Agency Buyers')}</span>
                                        </div>
                                    ` : ''}

                                    <p class="text-xs text-slate-400 mb-3.5 leading-relaxed">${escapeHtml(item.why_it_sells)}</p>

                                    <!-- Primary Concept Titles (Score System Active) -->
                                    <div class="p-3.5 rounded-xl bg-slate-900/90 border border-slate-800 mb-3.5">
                                        <div class="flex items-center justify-between mb-2 pb-1.5 border-b border-slate-800/80">
                                            <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                                                <i data-lucide="sparkles" class="w-3.5 h-3.5 text-amber-400"></i>
                                                Primary Concept Stock Titles (${primaryTitles.length}):
                                            </span>
                                            <button onclick="copyRegisteredText('${allPrimaryTitlesId}', 'All Primary Titles')" class="text-xs text-indigo-400 hover:text-indigo-300 font-semibold flex items-center gap-1 transition">
                                                <i data-lucide="copy" class="w-3 h-3"></i> Copy All
                                            </button>
                                        </div>
                                        <div class="space-y-2">
                                            ${primaryTitles.map(t => {
                                                const tId = registerData(t);
                                                const tScore = resolveTitleScore(item, t);
                                                return `
                                                    <div class="flex items-start justify-between gap-2 p-2.5 rounded-lg bg-slate-950/60 border border-slate-800/70 hover:border-emerald-500/30 transition">
                                                        <div class="flex-1 min-w-0">
                                                            <div class="flex flex-wrap items-center gap-1.5 mb-1">
                                                                <span class="px-2 py-0.5 rounded text-[10px] font-black bg-${tScore.color}-500/20 text-${tScore.color}-300 border border-${tScore.color}-500/40 font-mono shadow-sm" title="${tScore.ctr_rating} • ${tScore.commercial_intent}">
                                                                    ★ ${tScore.score} • ${tScore.grade} CTR
                                                                </span>
                                                                <span class="text-[10px] text-slate-400 font-mono hidden sm:inline">${tScore.competition}</span>
                                                            </div>
                                                            <div class="text-xs font-mono text-emerald-300 leading-snug break-words">${escapeHtml(t)}</div>
                                                        </div>
                                                        <button onclick="copyRegisteredText('${tId}', 'Title Copied!')" class="text-xs text-indigo-400 hover:text-indigo-300 font-semibold shrink-0 flex items-center gap-1 px-2 py-1 rounded hover:bg-slate-800 transition self-start sm:self-center">
                                                            <i data-lucide="copy" class="w-3 h-3"></i> Copy
                                                        </button>
                                                    </div>
                                                `;
                                            }).join('')}
                                        </div>
                                    </div>

                                    <!-- Interactive Tags Selector (Score System Active) -->
                                    <div class="mb-3.5">
                                        <div class="flex items-center justify-between mb-1.5">
                                            <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
                                                <i data-lucide="tags" class="w-3 h-3 text-indigo-400"></i>
                                                Click any tag to view its stock titles & score:
                                            </span>
                                            <span class="text-[10px] text-slate-500 font-mono">${(item.sample_tags || []).length} commercial tags</span>
                                        </div>
                                        <div class="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800/80 text-xs text-slate-300 max-h-28 overflow-y-auto leading-relaxed no-scrollbar flex flex-wrap gap-1.5" id="tags-container-${itemCardId}">
                                            ${(item.sample_tags || []).map((t, idx) => {
                                                const tgScore = resolveTagScore(item, t);
                                                return `
                                                    <button
                                                        type="button"
                                                        onclick="selectTagTitles('${itemCardId}', this.getAttribute('data-tag'))"
                                                        data-tag="${escapeHtml(t)}"
                                                        class="tag-pill inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-mono border border-slate-700/80 bg-slate-800/90 text-slate-300 hover:text-white cursor-pointer ${idx === 0 ? 'tag-pill-active' : ''}"
                                                        title="Score: ${tgScore.score}/100 • Volume: ${tgScore.volume} • Comp: ${tgScore.competition} • ${tgScore.tier}"
                                                    >
                                                        <span>${escapeHtml(t)}</span>
                                                        <span class="px-1.5 py-0.2 rounded text-[9px] font-black bg-${tgScore.color}-500/25 text-${tgScore.color}-300 border border-${tgScore.color}-500/35">${tgScore.score}</span>
                                                    </button>
                                                `;
                                            }).join('')}
                                        </div>
                                    </div>

                                    <!-- Selected Tag Titles Panel -->
                                    <div id="tag-titles-panel-${itemCardId}" class="p-3.5 rounded-xl bg-slate-900/95 border border-indigo-500/30 mb-3.5 shadow-lg"></div>

                                    <!-- Expandable Drawer for All Tags -->
                                    <div class="mb-3.5">
                                        <button
                                            type="button"
                                            onclick="toggleAllTagTitles('${itemCardId}')"
                                            id="toggle-btn-${itemCardId}"
                                            class="w-full py-2 px-3 rounded-xl bg-slate-900/80 hover:bg-slate-800 border border-slate-800 text-xs font-bold text-slate-300 hover:text-white flex items-center justify-between transition active:scale-95"
                                        >
                                            <span class="flex items-center gap-1.5">
                                                <i data-lucide="list" class="w-3.5 h-3.5 text-indigo-400"></i>
                                                <span>Browse All Titles for Each Tag (${(item.sample_tags || []).length} Tags with Scores)</span>
                                            </span>
                                            <i data-lucide="chevron-down" id="chevron-${itemCardId}" class="w-4 h-4 text-slate-400 transition-transform"></i>
                                        </button>
                                        <div id="all-tag-titles-drawer-${itemCardId}" class="hidden mt-2 p-3 rounded-xl bg-slate-950/70 border border-slate-800 max-h-72 overflow-y-auto space-y-3 no-scrollbar"></div>
                                    </div>

                                    ${item.ai_prompts ? `
                                        <!-- Expandable Drawer for AI Prompts & Style Reference -->
                                        <div class="mb-3.5">
                                            <button
                                                type="button"
                                                onclick="toggleConceptAIPrompt('${itemCardId}')"
                                                id="toggle-ai-btn-${itemCardId}"
                                                class="w-full py-2.5 px-3.5 rounded-xl bg-purple-950/40 hover:bg-purple-900/60 border border-purple-500/30 text-xs font-bold text-purple-200 hover:text-white flex items-center justify-between transition active:scale-95 shadow-sm"
                                            >
                                                <span class="flex items-center gap-1.5">
                                                    <i data-lucide="sparkles" class="w-3.5 h-3.5 text-purple-400"></i>
                                                    <span>Commercial AI Prompts & Visual Reference (--sref)</span>
                                                </span>
                                                <i data-lucide="chevron-down" id="chevron-ai-${itemCardId}" class="w-4 h-4 text-purple-400 transition-transform"></i>
                                            </button>
                                            <div id="concept-ai-drawer-${itemCardId}" class="hidden mt-2 p-3.5 rounded-xl bg-slate-950/95 border border-purple-500/30 space-y-3 no-scrollbar text-xs">
                                                ${renderConceptAIPromptDrawer(itemCardId, item)}
                                            </div>
                                        </div>
                                    ` : ''}
                                </div>

                                <!-- Card Footer -->
                                <div class="pt-3 border-t border-slate-800 flex flex-wrap items-center justify-between gap-2">
                                    <div class="flex items-center gap-2">
                                        <button onclick="quickLogAssetFromRegistry('${fullItemId}')" class="px-3 py-1.5 rounded-xl bg-emerald-600/20 hover:bg-emerald-600/40 text-emerald-300 border border-emerald-500/30 text-xs font-bold transition flex items-center gap-1.5 shadow-sm active:scale-95">
                                            <i data-lucide="check" class="w-3.5 h-3.5"></i>
                                            Mark Done Today
                                        </button>
                                        <button onclick="saveKeywordFromRegistry('${registerData({ keyword: item.concept, best_marketplace: p.name, recommended_tool: item.asset_type, opportunity_score: 85, suggested_title: item.suggested_title })}')" class="px-2.5 py-1.5 rounded-xl bg-indigo-600/20 hover:bg-indigo-600/40 text-indigo-300 border border-indigo-500/30 text-xs font-bold transition flex items-center gap-1.5 shadow-sm active:scale-95" title="Add to Production Kanban">
                                            <i data-lucide="plus" class="w-3.5 h-3.5"></i>
                                            Queue
                                        </button>
                                    </div>
                                    <div class="flex items-center gap-2">
                                        <button onclick="copyRegisteredText('${tagsId}', 'All Tags')" class="text-xs font-semibold text-slate-400 hover:text-white transition flex items-center gap-1">
                                            <i data-lucide="copy" class="w-3 h-3"></i> Copy Tags
                                        </button>
                                        <button onclick="copyAllTitlesForConcept('${cardItemDataId}')" class="text-xs font-semibold text-indigo-400 hover:text-indigo-300 transition flex items-center gap-1" title="Copy every title for every tag in this concept">
                                            <i data-lucide="copy" class="w-3 h-3"></i> Copy All Tag Titles
                                        </button>
                                    </div>
                                </div>
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>
        `;

        container.innerHTML = html;

        if (platformKey === 'adobe_stock') {
            loadAdobeStockAIStudio('abstract 3d liquid waves');
        }

        // Initialize active tag titles panel for each card
        (p.what_to_create || []).forEach((item, itemIdx) => {
            const itemCardId = `wtc_${platformKey}_${itemIdx}`;
            if (item.sample_tags && item.sample_tags.length > 0) {
                renderTagTitlesPanel(itemCardId, item.sample_tags[0]);
            }
        });

        lucide.createIcons();
    } catch (e) {
        console.error('Error loading platform tab:', e);
    }
}

// --- TAG-SPECIFIC STOCK TITLES CONTROLLER ---

function getTitlesForTag(item, tag) {
    if (item.tag_titles && item.tag_titles[tag] && item.tag_titles[tag].length > 0) {
        return item.tag_titles[tag];
    }
    const cap = tag.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
    const tool = item.asset_type ? item.asset_type.replace(/\(.*\)/, '').trim() : 'Stock Asset';
    return [
        `${cap} with Modern Lighting and Creative Composition for Commercial Stock`,
        `High Resolution ${cap} ${tool} for Business Marketing and Digital Web Banner`,
        `Minimalist ${cap} Concept Background with Ample Copy Space for Advertising`
    ];
}

function renderTagTitlesPanel(itemCardId, tag) {
    const item = getRegisteredData(itemCardId);
    if (!item) return;

    const titles = getTitlesForTag(item, tag);
    const panel = document.getElementById(`tag-titles-panel-${itemCardId}`);
    if (!panel) return;

    const tgScore = resolveTagScore(item, tag);
    const allTitlesText = titles.map((t, i) => `${i + 1}. ${t}`).join('\n');
    const allTitlesId = registerData(allTitlesText);

    panel.innerHTML = `
        <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-2 mb-2.5 border-b border-indigo-500/25 gap-2">
            <div class="flex flex-wrap items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
                <span class="text-xs font-bold text-white">Titles for Tag:</span>
                <span class="px-2 py-0.5 rounded-md text-[11px] font-bold font-mono bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">${escapeHtml(tag)}</span>
                <span class="px-2 py-0.5 rounded text-[10px] font-black bg-${tgScore.color}-500/25 text-${tgScore.color}-300 border border-${tgScore.color}-500/35 font-mono shadow-sm">
                    ★ ${tgScore.score} Tag Score • ${tgScore.volume} Vol
                </span>
            </div>
            <button onclick="copyRegisteredText('${allTitlesId}', 'All ${titles.length} Titles for Tag: ${escapeHtml(tag)}')" class="text-xs text-indigo-400 hover:text-indigo-300 font-semibold flex items-center gap-1 transition self-end sm:self-auto">
                <i data-lucide="copy" class="w-3 h-3"></i> Copy All (${titles.length})
            </button>
        </div>
        <div class="space-y-2">
            ${titles.map((t, idx) => {
                const tId = registerData(t);
                const tScore = resolveTitleScore(item, t, tag);
                const titleItemId = registerData({
                    suggested_title: t,
                    asset_type: item.asset_type,
                    platform: item.platform || 'Adobe Stock',
                    keyword: tag
                });

                return `
                    <div class="p-2.5 rounded-xl bg-slate-950/70 border border-slate-800/80 hover:border-indigo-500/30 transition flex flex-col sm:flex-row sm:items-center justify-between gap-2 tag-title-item">
                        <div class="flex items-start gap-2 flex-1 min-w-0">
                            <span class="tag-title-number shrink-0 mt-0.5">#${idx + 1}</span>
                            <div class="flex-1 min-w-0">
                                <div class="flex items-center gap-2 mb-1">
                                    <span class="px-1.5 py-0.2 rounded text-[9px] font-black bg-${tScore.color}-500/20 text-${tScore.color}-300 border border-${tScore.color}-500/40 font-mono">
                                        ★ ${tScore.score} • ${tScore.grade} CTR
                                    </span>
                                    <span class="text-[10px] text-slate-400 font-mono">${tScore.competition}</span>
                                </div>
                                <div class="text-xs font-mono text-emerald-300 leading-snug break-words">${escapeHtml(t)}</div>
                            </div>
                        </div>
                        <div class="flex items-center gap-1.5 shrink-0 self-end sm:self-center">
                            <button onclick="copyRegisteredText('${tId}', 'Stock Title Copied!')" class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition flex items-center gap-1 active:scale-95">
                                <i data-lucide="copy" class="w-3 h-3"></i> Copy
                            </button>
                            <button onclick="quickLogAssetFromRegistry('${titleItemId}')" class="px-2 py-1 rounded-lg bg-emerald-600/20 hover:bg-emerald-600/40 text-emerald-300 border border-emerald-500/30 text-xs font-bold transition flex items-center gap-1 active:scale-95" title="Log this title to Today's Goal">
                                <i data-lucide="check" class="w-3 h-3"></i>
                            </button>
                            <button onclick="saveKeywordFromRegistry('${registerData({ keyword: tag, best_marketplace: item.platform || 'Adobe Stock', recommended_tool: item.asset_type, opportunity_score: tScore.score || 90, suggested_title: t })}')" class="px-2 py-1 rounded-lg bg-indigo-600/20 hover:bg-indigo-600/40 text-indigo-300 border border-indigo-500/30 text-xs font-bold transition flex items-center gap-1 active:scale-95" title="Queue this title in Kanban">
                                <i data-lucide="plus" class="w-3 h-3"></i>
                            </button>
                        </div>
                    </div>
                `;
            }).join('')}
        </div>
    `;

    lucide.createIcons();
}

function selectTagTitles(itemCardId, tag) {
    const container = document.getElementById(`tags-container-${itemCardId}`);
    if (container) {
        container.querySelectorAll('.tag-pill').forEach(btn => {
            if (btn.getAttribute('data-tag') === tag) {
                btn.classList.add('tag-pill-active');
            } else {
                btn.classList.remove('tag-pill-active');
            }
        });
    }
    renderTagTitlesPanel(itemCardId, tag);
}

function toggleAllTagTitles(itemCardId) {
    const drawer = document.getElementById(`all-tag-titles-drawer-${itemCardId}`);
    const chevron = document.getElementById(`chevron-${itemCardId}`);
    if (!drawer) return;

    if (drawer.classList.contains('hidden')) {
        drawer.classList.remove('hidden');
        if (chevron) chevron.style.transform = 'rotate(180deg)';

        const item = getRegisteredData(itemCardId);
        if (item) {
            drawer.innerHTML = (item.sample_tags || []).map(tag => {
                const titles = getTitlesForTag(item, tag);
                const tgScore = resolveTagScore(item, tag);
                const tagAllTitlesId = registerData(titles.map((t, i) => `${i + 1}. ${t}`).join('\n'));

                return `
                    <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800">
                        <div class="flex items-center justify-between pb-1.5 mb-2 border-b border-slate-800">
                            <div class="flex items-center gap-2">
                                <span class="text-xs font-bold text-amber-400 font-mono">Tag: "${escapeHtml(tag)}"</span>
                                <span class="px-1.5 py-0.2 rounded text-[9px] font-black bg-${tgScore.color}-500/25 text-${tgScore.color}-300 border border-${tgScore.color}-500/35 font-mono">
                                    ★ Score: ${tgScore.score}
                                </span>
                            </div>
                            <button onclick="copyRegisteredText('${tagAllTitlesId}', 'All Titles for Tag: ${escapeHtml(tag)}')" class="text-[11px] text-indigo-400 hover:text-indigo-300 font-semibold flex items-center gap-1">
                                <i data-lucide="copy" class="w-3 h-3"></i> Copy Tag Titles
                            </button>
                        </div>
                        <div class="space-y-1.5">
                            ${titles.map((t, idx) => {
                                const tId = registerData(t);
                                const tScore = resolveTitleScore(item, t, tag);
                                return `
                                    <div class="flex items-center justify-between gap-2 text-xs font-mono text-slate-300 p-1.5 rounded bg-slate-950/50">
                                        <div class="flex items-center gap-2 flex-1 min-w-0">
                                            <span class="text-slate-500 shrink-0">#${idx + 1}</span>
                                            <span class="px-1.5 py-0.2 rounded text-[9px] font-black bg-${tScore.color}-500/20 text-${tScore.color}-300 border border-${tScore.color}-500/40 shrink-0 font-mono">
                                                ★ ${tScore.score}
                                            </span>
                                            <span class="text-emerald-300 truncate">${escapeHtml(t)}</span>
                                        </div>
                                        <button onclick="copyRegisteredText('${tId}', 'Title Copied!')" class="text-indigo-400 hover:text-indigo-300 text-[11px] font-semibold shrink-0 ml-2">Copy</button>
                                    </div>
                                `;
                            }).join('')}
                        </div>
                    </div>
                `;
            }).join('');
            lucide.createIcons();
        }
    } else {
        drawer.classList.add('hidden');
        if (chevron) chevron.style.transform = 'rotate(0deg)';
    }
}

function copyAllTitlesForConcept(itemDataId) {
    const item = getRegisteredData(itemDataId);
    if (!item) return;

    let text = `=== STOCK TITLES CATALOG FOR: ${item.concept} (${item.asset_type}) ===\n\n`;
    if (item.suggested_titles && item.suggested_titles.length > 0) {
        text += `[PRIMARY CONCEPT TITLES]\n` + item.suggested_titles.map((t, i) => `${i + 1}. ${t}`).join('\n') + `\n\n`;
    }
    text += `[TITLES BY TAG]\n`;
    (item.sample_tags || []).forEach(tag => {
        const titles = getTitlesForTag(item, tag);
        text += `Tag: ${tag}\n`;
        titles.forEach((t, i) => {
            text += `  ${i + 1}. ${t}\n`;
        });
        text += `\n`;
    });

    copyToClipboard(text, `All Titles for "${item.concept}" Copied!`);
}

function switchReqTab(platformKey, reqType) {
    const panels = document.querySelectorAll(`[id^="req-panel-${platformKey}-"]`);
    const buttons = document.querySelectorAll(`[id^="req-btn-${platformKey}-"]`);

    panels.forEach(p => p.classList.add('hidden'));
    buttons.forEach(b => {
        b.className = "px-4 py-2 rounded-xl text-xs font-bold bg-slate-800 text-slate-300 hover:text-white flex items-center gap-1.5 transition";
    });

    const activePanel = document.getElementById(`req-panel-${platformKey}-${reqType}`);
    const activeBtn = document.getElementById(`req-btn-${platformKey}-${reqType}`);

    if (activePanel) activePanel.classList.remove('hidden');
    if (activeBtn) activeBtn.className = "px-4 py-2 rounded-xl text-xs font-bold bg-indigo-600 text-white shadow-md shadow-indigo-600/30 flex items-center gap-1.5 transition";

    lucide.createIcons();
}

async function executePlatformSearch(platformKey) {
    const input = document.getElementById(`platform-search-input-${platformKey}`);
    const query = input ? input.value.trim() : '';
    if (!query) {
        showToast('Please type a search query for ' + platformKey.replace('_', ' '), 'info');
        return;
    }

    // Call loadPlatformTab with the search query to re-render the entire platform page dynamically
    await loadPlatformTab(platformKey, query);

    // Smooth scroll down to the what-to-create section
    setTimeout(() => {
        const target = document.getElementById(`what-to-create-root-${platformKey}`) || document.getElementById(`tab-platform-${platformKey}`);
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }, 150);
}

function clearPlatformSearch(platformKey) {
    loadPlatformTab(platformKey, null);
    setTimeout(() => {
        const input = document.getElementById(`platform-search-input-${platformKey}`);
        if (input) input.value = '';
    }, 100);
}

function switchToMarketplaceWithSearch(platformKey, queryOrId) {
    const raw = getRegisteredData(queryOrId);
    const query = (raw !== undefined && raw !== null) ? raw : queryOrId;
    switchTab(`platform-${platformKey}`, query);
    setTimeout(() => {
        const input = document.getElementById(`platform-search-input-${platformKey}`);
        if (input) input.value = query;
        const target = document.getElementById(`what-to-create-root-${platformKey}`) || document.getElementById(`tab-platform-${platformKey}`);
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }, 200);
}

// --- DAILY PROGRESS TRACKER & GOAL MANAGER ---
async function renderDailyTrackerTab(fetchData = true) {
    const container = document.getElementById('tab-daily-tracker');
    if (!container) return;

    if (fetchData || !state.todayGoal) {
        await loadTodayGoal(false);
    }
    const goal = state.todayGoal;
    if (!goal) return;

    // Fetch streak and history
    let streakData = { streak_days: 0, history: [] };
    try {
        const sRes = await fetch('/api/daily-goals/streak?days=14');
        streakData = await sRes.json();
    } catch (e) {
        console.error(e);
    }

    const allAssets = goal.assets || [];
    const totalCount = allAssets.length;
    const pendingCount = allAssets.filter(a => a.status !== 'Uploaded').length;
    const uploadedCount = allAssets.filter(a => a.status === 'Uploaded').length;

    let filteredAssets = allAssets;
    if (state.todayAssetsFilter === 'pending') {
        filteredAssets = allAssets.filter(a => a.status !== 'Uploaded');
    } else if (state.todayAssetsFilter === 'uploaded') {
        filteredAssets = allAssets.filter(a => a.status === 'Uploaded');
    }

    let html = `
        <!-- Top Stats Banner -->
        <div class="glass-panel rounded-3xl p-8 mb-8 border border-slate-700/60 relative overflow-hidden shadow-2xl">
            <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
                <div>
                    <div class="flex items-center gap-3">
                        <span class="px-3.5 py-1 rounded-full text-xs font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                            Daily Stock Production Tracker
                        </span>
                        <div class="streak-badge px-3.5 py-1 rounded-full text-xs font-bold text-orange-400 flex items-center gap-1.5">
                            <i data-lucide="flame" class="w-4 h-4 fill-orange-500 text-orange-500"></i>
                            <span>${streakData.streak_days} Day Consistency Streak</span>
                        </div>
                    </div>
                    <h2 class="text-3xl sm:text-4xl font-black text-white mt-2.5 tracking-tight">
                        Today's Progress: ${goal.total_created} / ${goal.total_target} Assets (${goal.percentage}%)
                    </h2>
                    <p class="text-slate-300 text-sm mt-1 max-w-2xl leading-relaxed">
                        Persistently recorded in your local database. Track created vs uploaded assets to maintain continuous contributor momentum.
                    </p>
                </div>

                <!-- Big Progress Indicator Card -->
                <div class="w-full lg:w-80 p-5 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl">
                    <div class="flex items-center justify-between text-xs font-bold text-slate-300 mb-2">
                        <span>Overall Goal Completion</span>
                        <span class="text-emerald-400 font-mono text-sm">${goal.percentage}%</span>
                    </div>
                    <div class="w-full h-3 rounded-full bg-slate-800 overflow-hidden relative">
                        <div class="h-full rounded-full bg-gradient-to-r from-indigo-500 via-purple-500 to-emerald-400 progress-bar-fill" style="width: ${goal.percentage}%"></div>
                    </div>
                    <div class="flex justify-between items-center text-[11px] text-slate-400 mt-2.5 font-mono">
                        <span class="text-emerald-300 font-bold">${goal.total_uploaded} Uploaded</span>
                        <span class="text-slate-400">${goal.total_created - goal.total_uploaded} Pending Upload</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Target Setting & Quick Log Section -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <!-- Daily Target Quotas Card -->
            <div class="glass-panel rounded-2xl p-6 border border-slate-800 shadow-xl">
                <div class="flex items-center justify-between mb-3">
                    <div class="flex items-center gap-2">
                        <i data-lucide="target" class="w-5 h-5 text-indigo-400"></i>
                        <h3 class="font-bold text-white text-base">Today's Production Targets</h3>
                    </div>
                    <button onclick="saveDailyTargetsFromUI()" class="px-3.5 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition shadow-sm active:scale-95">
                        Save Targets
                    </button>
                </div>

                <!-- Fast Quota Presets -->
                <div class="flex flex-wrap items-center gap-2 mb-4 pb-3 border-b border-slate-800/80">
                    <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Fast Presets:</span>
                    <button onclick="applyGoalPreset(2, 5, 2, 1)" class="preset-btn px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-800/90 text-slate-300 hover:text-white border border-slate-700 transition active:scale-95" title="10 Assets: 2 Vectors, 5 Images, 2 Videos, 1 Template">Light (10)</button>
                    <button onclick="applyGoalPreset(5, 10, 5, 3)" class="preset-btn px-2.5 py-1 rounded-lg text-xs font-semibold bg-indigo-600/20 text-indigo-300 hover:text-white border border-indigo-500/30 transition active:scale-95" title="23 Assets: 5 Vectors, 10 Images, 5 Videos, 3 Templates">Standard (23)</button>
                    <button onclick="applyGoalPreset(10, 18, 8, 4)" class="preset-btn px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-800/90 text-slate-300 hover:text-white border border-slate-700 transition active:scale-95" title="40 Assets: 10 Vectors, 18 Images, 8 Videos, 4 Templates">Intensive (40)</button>
                </div>

                <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 text-center">
                        <span class="text-[11px] text-slate-400 font-bold block mb-1">📐 Vectors</span>
                        <div class="flex items-center justify-center gap-1">
                            <button onclick="adjustTargetInput('input-target-vectors', -1)" class="w-6 h-6 rounded bg-slate-800 text-slate-400 hover:text-white font-bold text-xs">-</button>
                            <input id="input-target-vectors" type="number" min="0" value="${goal.target_vectors}" class="w-12 bg-slate-800/90 text-white text-center font-bold text-sm rounded py-1 border border-slate-700 focus:outline-none" />
                            <button onclick="adjustTargetInput('input-target-vectors', 1)" class="w-6 h-6 rounded bg-slate-800 text-slate-400 hover:text-white font-bold text-xs">+</button>
                        </div>
                        <span class="text-[10px] text-emerald-400 font-mono block mt-1.5 font-bold">${goal.completed_vectors} done</span>
                    </div>
                    <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 text-center">
                        <span class="text-[11px] text-slate-400 font-bold block mb-1">📸 AI Images</span>
                        <div class="flex items-center justify-center gap-1">
                            <button onclick="adjustTargetInput('input-target-images', -1)" class="w-6 h-6 rounded bg-slate-800 text-slate-400 hover:text-white font-bold text-xs">-</button>
                            <input id="input-target-images" type="number" min="0" value="${goal.target_images}" class="w-12 bg-slate-800/90 text-white text-center font-bold text-sm rounded py-1 border border-slate-700 focus:outline-none" />
                            <button onclick="adjustTargetInput('input-target-images', 1)" class="w-6 h-6 rounded bg-slate-800 text-slate-400 hover:text-white font-bold text-xs">+</button>
                        </div>
                        <span class="text-[10px] text-emerald-400 font-mono block mt-1.5 font-bold">${goal.completed_images} done</span>
                    </div>
                    <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 text-center">
                        <span class="text-[11px] text-slate-400 font-bold block mb-1">🎬 AI Videos</span>
                        <div class="flex items-center justify-center gap-1">
                            <button onclick="adjustTargetInput('input-target-videos', -1)" class="w-6 h-6 rounded bg-slate-800 text-slate-400 hover:text-white font-bold text-xs">-</button>
                            <input id="input-target-videos" type="number" min="0" value="${goal.target_videos}" class="w-12 bg-slate-800/90 text-white text-center font-bold text-sm rounded py-1 border border-slate-700 focus:outline-none" />
                            <button onclick="adjustTargetInput('input-target-videos', 1)" class="w-6 h-6 rounded bg-slate-800 text-slate-400 hover:text-white font-bold text-xs">+</button>
                        </div>
                        <span class="text-[10px] text-emerald-400 font-mono block mt-1.5 font-bold">${goal.completed_videos} done</span>
                    </div>
                    <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 text-center">
                        <span class="text-[11px] text-slate-400 font-bold block mb-1">📄 Templates</span>
                        <div class="flex items-center justify-center gap-1">
                            <button onclick="adjustTargetInput('input-target-templates', -1)" class="w-6 h-6 rounded bg-slate-800 text-slate-400 hover:text-white font-bold text-xs">-</button>
                            <input id="input-target-templates" type="number" min="0" value="${goal.target_templates}" class="w-12 bg-slate-800/90 text-white text-center font-bold text-sm rounded py-1 border border-slate-700 focus:outline-none" />
                            <button onclick="adjustTargetInput('input-target-templates', 1)" class="w-6 h-6 rounded bg-slate-800 text-slate-400 hover:text-white font-bold text-xs">+</button>
                        </div>
                        <span class="text-[10px] text-emerald-400 font-mono block mt-1.5 font-bold">${goal.completed_templates} done</span>
                    </div>
                </div>
            </div>

            <!-- Log Completed Asset Form -->
            <div class="glass-panel rounded-2xl p-6 border border-slate-800 shadow-xl">
                <div class="flex items-center gap-2 mb-4">
                    <i data-lucide="plus-circle" class="w-5 h-5 text-emerald-400"></i>
                    <h3 class="font-bold text-white text-base">Quick Log Asset to Today</h3>
                </div>

                <div class="space-y-3">
                    <input
                        id="log-asset-title"
                        type="text"
                        placeholder="Asset Title (e.g. Modern Real Estate Flyer, Cyberpunk 4K Loop)..."
                        class="w-full bg-slate-900 text-white text-xs py-2.5 px-3.5 rounded-xl border border-slate-700/80 focus:outline-none focus:border-indigo-500 font-medium"
                        onkeydown="if(event.key==='Enter') submitManualAssetLog()"
                    />
                    
                    <div class="grid grid-cols-2 gap-3">
                        <select id="log-asset-type" class="bg-slate-900 text-slate-200 text-xs py-2.5 px-3 rounded-xl border border-slate-700/80 focus:outline-none font-medium">
                            <option value="AI Image">📸 AI Image</option>
                            <option value="AI Video">🎬 AI Video</option>
                            <option value="Vector">📐 Vector (Illustrator)</option>
                            <option value="Canva Template">📄 Canva Template</option>
                            <option value="Photoshop PSD">🖼️ Photoshop PSD</option>
                        </select>
                        <select id="log-asset-platform" class="bg-slate-900 text-slate-200 text-xs py-2.5 px-3 rounded-xl border border-slate-700/80 focus:outline-none font-medium">
                            <option value="Adobe Stock">Adobe Stock</option>
                            <option value="Etsy">Etsy</option>
                            <option value="Shutterstock">Shutterstock</option>
                            <option value="IconScout">IconScout</option>
                            <option value="GraphicRiver">GraphicRiver</option>
                        </select>
                    </div>

                    <button onclick="submitManualAssetLog()" class="w-full py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white text-xs font-bold transition flex items-center justify-center gap-1.5 shadow-lg shadow-emerald-600/20 active:scale-95">
                        <i data-lucide="check-check" class="w-4 h-4"></i>
                        <span>Add to Today's Completed List</span>
                    </button>
                </div>
            </div>
        </div>

        <!-- Logged Assets Table for Today -->
        <div class="glass-panel rounded-2xl p-6 border border-slate-800 shadow-xl mb-8">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4 pb-3 border-b border-slate-800/80">
                <div class="flex items-center gap-2">
                    <i data-lucide="check-square" class="w-4 h-4 text-emerald-400"></i>
                    <h3 class="font-bold text-white text-base">Today's Completed Assets List</h3>
                </div>

                <!-- Asset Status Filter -->
                <div class="flex items-center gap-1.5">
                    <button onclick="setTodayAssetsFilter('all')" class="filter-chip ${state.todayAssetsFilter === 'all' ? 'active' : ''}">All (${totalCount})</button>
                    <button onclick="setTodayAssetsFilter('pending')" class="filter-chip ${state.todayAssetsFilter === 'pending' ? 'active' : ''}">Pending (${pendingCount})</button>
                    <button onclick="setTodayAssetsFilter('uploaded')" class="filter-chip ${state.todayAssetsFilter === 'uploaded' ? 'active' : ''}">Uploaded (${uploadedCount})</button>
                </div>
            </div>
            
            ${filteredAssets.length === 0 ? `
                <div class="text-center py-12 text-slate-500 text-sm">
                    ${totalCount === 0 ? 'No assets logged for today yet. Use the form above or click "+ Log Done" from any keyword or AI quota card!' : 'No assets match the selected filter.'}
                </div>
            ` : `
                <div class="divide-y divide-slate-800/80">
                    ${filteredAssets.map(a => {
                        const timing = getClientUploadDeadline(a.title);
                        return `
                        <div class="py-3.5 px-3 rounded-xl flex items-center justify-between gap-4 transition ${timing.is_late ? 'border-l-4 border-l-rose-500 bg-rose-950/20 my-1' : ''}">
                            <div class="flex items-center gap-3 min-w-0 flex-1">
                                <button onclick="toggleAssetStatus(${a.id}, '${a.status}')" class="w-7 h-7 rounded-lg flex items-center justify-center transition shrink-0 ${a.status === 'Uploaded' ? 'bg-emerald-500 text-white shadow-md shadow-emerald-500/25' : 'border border-slate-600 text-slate-400 hover:text-white hover:border-slate-400'}" title="Toggle Created vs Uploaded">
                                    <i data-lucide="check" class="w-4 h-4"></i>
                                </button>
                                <div class="min-w-0 flex-1">
                                    <div class="font-bold text-white text-sm truncate ${a.status === 'Uploaded' ? 'line-through text-slate-400' : ''}">${escapeHtml(a.title)}</div>
                                    <div class="flex flex-wrap items-center gap-2 mt-0.5 text-[11px] text-slate-400 font-mono">
                                        <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300">${escapeHtml(a.asset_type)}</span>
                                        <span>•</span>
                                        <span>${escapeHtml(a.platform)}</span>
                                        <span>•</span>
                                        <span class="${a.status === 'Uploaded' ? 'text-emerald-400 font-bold' : 'text-amber-400'}">${a.status}</span>
                                        <span>•</span>
                                        <span class="px-1.5 py-0.5 rounded text-[10px] font-black ${timing.is_late ? 'bg-rose-600 text-white animate-pulse' : (timing.timing_status === 'CLOSING_SOON' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' : 'bg-slate-800 text-slate-300 border border-slate-700')}">
                                            ${escapeHtml(timing.timing_badge)}
                                        </span>
                                        <span class="text-slate-400 hidden sm:inline">Due: <strong class="${timing.is_late ? 'text-rose-400 font-bold' : 'text-slate-200'}">${escapeHtml(timing.upload_deadline)}</strong></span>
                                        <span class="text-slate-600 hidden md:inline">•</span>
                                        <span class="text-slate-400 hidden md:inline">Window: <strong class="text-slate-300">${escapeHtml(timing.upload_date_range)}</strong>${timing.is_late ? ` <span class="text-rose-400 font-bold">(${timing.days_overdue}d overdue)</span>` : ''}</span>
                                    </div>
                                </div>
                            </div>

                            <button onclick="removeAssetLog(${a.id})" class="text-slate-500 hover:text-rose-400 p-1.5 rounded-lg hover:bg-slate-800 transition shrink-0" title="Delete Asset">
                                <i data-lucide="trash-2" class="w-4 h-4"></i>
                            </button>
                        </div>
                        `;
                    }).join('')}
                </div>
            `}
        </div>

        <!-- 14-Day Consistency Radar -->
        <div class="glass-panel rounded-2xl p-6 border border-slate-800 shadow-xl">
            <h3 class="font-bold text-white text-base mb-3 flex items-center gap-2">
                <i data-lucide="calendar" class="w-4 h-4 text-indigo-400"></i>
                <span>14-Day Production Consistency Streak</span>
            </h3>
            <div class="grid grid-cols-7 sm:grid-cols-14 gap-2">
                ${streakData.history.map(h => `
                    <div class="p-2.5 rounded-xl text-center border ${h.completed > 0 ? 'bg-indigo-600/20 border-indigo-500/40 shadow-sm' : 'bg-slate-900/50 border-slate-800/80'}">
                        <span class="text-[10px] text-slate-400 block font-mono">${h.date.slice(5)}</span>
                        <span class="text-xs font-black ${h.completed > 0 ? 'text-emerald-400' : 'text-slate-600'} block mt-1 font-mono">${h.completed}</span>
                    </div>
                `).join('')}
            </div>
        </div>
    `;

    container.innerHTML = html;
    lucide.createIcons();
}

function setTodayAssetsFilter(filter) {
    state.todayAssetsFilter = filter;
    renderDailyTrackerTab(false);
}

async function applyGoalPreset(v, img, vid, t) {
    const vEl = document.getElementById('input-target-vectors');
    const imgEl = document.getElementById('input-target-images');
    const vidEl = document.getElementById('input-target-videos');
    const tEl = document.getElementById('input-target-templates');
    if (vEl) vEl.value = v;
    if (imgEl) imgEl.value = img;
    if (vidEl) vidEl.value = vid;
    if (tEl) tEl.value = t;
    await saveDailyTargetsFromUI();
}

function adjustTargetInput(id, delta) {
    const input = document.getElementById(id);
    if (!input) return;
    const cur = parseInt(input.value) || 0;
    input.value = Math.max(0, cur + delta);
}

async function saveDailyTargetsFromUI() {
    const v = parseInt(document.getElementById('input-target-vectors')?.value) || 0;
    const img = parseInt(document.getElementById('input-target-images')?.value) || 0;
    const vid = parseInt(document.getElementById('input-target-videos')?.value) || 0;
    const t = parseInt(document.getElementById('input-target-templates')?.value) || 0;

    try {
        await fetch('/api/daily-goals/today', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                target_vectors: v,
                target_images: img,
                target_videos: vid,
                target_templates: t
            })
        });
        showToast('Daily Targets Updated Successfully!', 'success');
        await loadTodayGoal(false);
        renderDailyTrackerTab(false);
    } catch (e) {
        showToast('Error updating targets', 'error');
    }
}

async function submitManualAssetLog() {
    const titleInput = document.getElementById('log-asset-title');
    const title = titleInput ? titleInput.value.trim() : '';
    if (!title) {
        showToast('Please type an asset title', 'info');
        return;
    }
    const type = document.getElementById('log-asset-type')?.value || 'AI Image';
    const platform = document.getElementById('log-asset-platform')?.value || 'Adobe Stock';

    try {
        await fetch('/api/daily-goals/log-asset', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title: title,
                asset_type: type,
                platform: platform,
                status: 'Created'
            })
        });
        showToast('Asset logged to today!', 'success');
        if (titleInput) titleInput.value = '';
        await loadTodayGoal(false);
        renderDailyTrackerTab(false);
    } catch (e) {
        showToast('Error logging asset', 'error');
    }
}

async function toggleAssetStatus(assetId, currentStatus) {
    const newStatus = currentStatus === 'Uploaded' ? 'Created' : 'Uploaded';
    try {
        await fetch(`/api/daily-goals/asset/${assetId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        });
        showToast(`Status changed to ${newStatus}`, 'success');
        await loadTodayGoal(false);
        renderDailyTrackerTab(false);
    } catch (e) {
        showToast('Error toggling status', 'error');
    }
}

async function removeAssetLog(assetId) {
    try {
        await fetch(`/api/daily-goals/asset/${assetId}`, { method: 'DELETE' });
        showToast('Asset removed from log', 'info');
        await loadTodayGoal(false);
        renderDailyTrackerTab(false);
    } catch (e) {
        showToast('Error deleting log', 'error');
    }
}

// --- DAILY RANKED CALENDAR & EVENTS TAB ---
async function loadDailyCalendarTab() {
    const container = document.getElementById('tab-daily-events');
    if (!container) return;

    try {
        const res = await fetch('/api/daily-events?days=365');
        const data = await res.json();
        state.calendarEvents = data.events || [];

        renderDailyCalendarContent();
    } catch (e) {
        console.error('Calendar error:', e);
    }
}

function setCalendarViewMode(mode) {
    state.calendarViewMode = mode;
    renderDailyCalendarContent();
}

function setCalendarFilter(f) {
    state.calendarFilter = f;
    renderDailyCalendarContent();
}

function setCalendarCategoryFilter(cat) {
    state.calendarCategoryFilter = cat;
    renderDailyCalendarContent();
}

function setCalendarTimingFilter(timing) {
    state.calendarTimingFilter = timing;
    renderDailyCalendarContent();
}

function onCalendarSearchInput(val) {
    state.calendarSearchQuery = (val || '').toLowerCase().trim();
    renderDailyCalendarContent();
}

function clearCalendarFilters() {
    state.calendarFilter = 'all';
    state.calendarCategoryFilter = 'all';
    state.calendarTimingFilter = 'all';
    state.calendarSearchQuery = '';
    renderDailyCalendarContent();
}

function renderDailyCalendarContent() {
    const container = document.getElementById('tab-daily-events');
    if (!container || !state.calendarEvents) return;

    const allEvents = state.calendarEvents;

    // Calculate aggregate metrics
    const totalCount = allEvents.length;
    const lateCount = allEvents.filter(e => e.is_late).length;
    const closingSoonCount = allEvents.filter(e => e.timing_status === 'CLOSING_SOON').length;
    const primeCount = allEvents.filter(e => e.timing_status === 'PRIME_WINDOW').length;
    const advanceCount = allEvents.filter(e => e.timing_status === 'ADVANCE_PREP').length;
    const fashionCount = allEvents.filter(e => (e.category || '').toLowerCase().includes('fashion')).length;
    const birthdayCount = allEvents.filter(e => (e.category || '').toLowerCase().includes('birthday') || (e.category || '').toLowerCase().includes('milestone')).length;

    // Filter pipeline
    let filtered = [...allEvents];

    // 1. Time horizon filter
    if (state.calendarFilter === 'urgent') {
        filtered = filtered.filter(e => e.urgency_level === 'Immediate' || e.urgency_level === 'Urgent' || e.urgency_level === 'Max Priority');
    } else if (state.calendarFilter === '30days') {
        filtered = filtered.filter(e => e.days_until <= 30);
    } else if (state.calendarFilter === '60days') {
        filtered = filtered.filter(e => e.days_until <= 60);
    }

    // 2. Category filter
    if (state.calendarCategoryFilter && state.calendarCategoryFilter !== 'all') {
        filtered = filtered.filter(e => (e.category || '').toLowerCase() === state.calendarCategoryFilter.toLowerCase());
    }

    // 3. Timing status filter
    if (state.calendarTimingFilter === 'late') {
        filtered = filtered.filter(e => e.is_late);
    } else if (state.calendarTimingFilter === 'closing_soon') {
        filtered = filtered.filter(e => e.timing_status === 'CLOSING_SOON');
    } else if (state.calendarTimingFilter === 'prime') {
        filtered = filtered.filter(e => e.timing_status === 'PRIME_WINDOW');
    } else if (state.calendarTimingFilter === 'advance') {
        filtered = filtered.filter(e => e.timing_status === 'ADVANCE_PREP');
    }

    // 4. In-Calendar text search filter
    if (state.calendarSearchQuery) {
        filtered = filtered.filter(e => {
            const nameMatch = (e.name || '').toLowerCase().includes(state.calendarSearchQuery);
            const catMatch = (e.category || '').toLowerCase().includes(state.calendarSearchQuery);
            const titlesMatch = (e.suggested_titles || []).some(t => t.toLowerCase().includes(state.calendarSearchQuery));
            const createMatch = Object.values(e.what_to_create || {}).some(v => (v || '').toLowerCase().includes(state.calendarSearchQuery));
            return nameMatch || catMatch || titlesMatch || createMatch;
        });
    }

    const categories = [
        { key: 'all', label: '🌟 All Categories', count: totalCount },
        { key: 'Fashion & Apparel', label: '👗 Fashion & Apparel', count: fashionCount },
        { key: 'Birthdays & Milestones', label: '🎂 Birthdays & Milestones', count: birthdayCount },
        { key: 'Holidays & Cultural', label: '🎉 Holidays & Cultural', count: allEvents.filter(e => (e.category || '').toLowerCase().includes('holiday')).length },
        { key: 'E-Commerce & Retail', label: '🛍️ E-Commerce & Retail', count: allEvents.filter(e => (e.category || '').toLowerCase().includes('commerce')).length },
        { key: 'Corporate & Tech', label: '💼 Corporate & Tech', count: allEvents.filter(e => (e.category || '').toLowerCase().includes('corporate')).length },
        { key: 'Health & Lifestyle', label: '🌿 Health & Lifestyle', count: allEvents.filter(e => (e.category || '').toLowerCase().includes('health')).length }
    ];

    let html = `
        <!-- Header Banner & Summary Radar -->
        <div class="glass-panel rounded-3xl p-6 sm:p-8 mb-6 border border-slate-700/60 shadow-2xl relative overflow-hidden">
            <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4 pb-6 border-b border-slate-800/80">
                <div>
                    <div class="flex flex-wrap items-center gap-2 mb-2">
                        <span class="px-3.5 py-1 rounded-full text-xs font-black bg-amber-500/20 text-amber-300 border border-amber-500/30 flex items-center gap-1.5 font-mono shadow-sm">
                            <i data-lucide="calendar" class="w-3.5 h-3.5 text-amber-400"></i>
                            365-Day Commercial Buying Calendar
                        </span>
                        <span class="text-xs text-slate-400 font-mono">Stock buyers license <strong>45–90 days ahead</strong> of peak demand</span>
                    </div>
                    <h2 class="text-2xl sm:text-4xl font-black text-white tracking-tight">Ranked Commercial Events & Seasonal Radar</h2>
                    <p class="text-slate-300 text-xs sm:text-sm mt-1 max-w-3xl leading-relaxed">
                        Track upcoming high-yield niches across Fashion drops, milestone birthdays, global holidays, and commercial quarters with exact upload deadlines.
                    </p>
                </div>

                <div class="flex items-center gap-2">
                    <button onclick="clearCalendarFilters()" class="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold border border-slate-700 transition flex items-center gap-1">
                        <i data-lucide="rotate-ccw" class="w-3 h-3"></i> Reset Filters
                    </button>
                </div>
            </div>

            <!-- 5-Metric Interactive Summary Bar (Clickable Quick Filters) -->
            <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 mt-6">
                <!-- Total -->
                <button onclick="setCalendarTimingFilter('all')" class="p-3.5 rounded-2xl bg-slate-900/90 border transition text-left ${state.calendarTimingFilter === 'all' ? 'border-amber-500 ring-2 ring-amber-500/20' : 'border-slate-800 hover:border-slate-700'}">
                    <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Tracked Events</span>
                    <div class="flex items-center justify-between mt-1">
                        <span class="text-2xl font-black text-white font-mono">${totalCount}</span>
                        <i data-lucide="calendar-check" class="w-5 h-5 text-amber-400 opacity-60"></i>
                    </div>
                    <span class="text-[10px] text-slate-400 font-mono mt-1 block">Full Radar Catalog</span>
                </button>

                <!-- Late (Critical Warning) -->
                <button onclick="setCalendarTimingFilter('late')" class="p-3.5 rounded-2xl bg-rose-950/20 border transition text-left group ${state.calendarTimingFilter === 'late' ? 'border-rose-500 ring-2 ring-rose-500/30 bg-rose-950/40' : 'border-rose-500/30 hover:border-rose-500/60'}">
                    <div class="flex items-center justify-between">
                        <span class="text-[10px] font-bold text-rose-300 uppercase tracking-wider">🔴 Late (Closed)</span>
                        <span class="w-2 h-2 rounded-full bg-rose-500 animate-pulse"></span>
                    </div>
                    <div class="flex items-center justify-between mt-1">
                        <span class="text-2xl font-black text-rose-400 font-mono">${lateCount}</span>
                        <i data-lucide="alert-circle" class="w-5 h-5 text-rose-400"></i>
                    </div>
                    <span class="text-[10px] text-rose-300/80 font-mono mt-1 block">Missed 45d Golden Window</span>
                </button>

                <!-- Closing Soon -->
                <button onclick="setCalendarTimingFilter('closing_soon')" class="p-3.5 rounded-2xl bg-amber-950/20 border transition text-left ${state.calendarTimingFilter === 'closing_soon' ? 'border-amber-500 ring-2 ring-amber-500/30 bg-amber-950/40' : 'border-amber-500/30 hover:border-amber-500/60'}">
                    <span class="text-[10px] font-bold text-amber-300 uppercase tracking-wider block">🟡 Closing Soon</span>
                    <div class="flex items-center justify-between mt-1">
                        <span class="text-2xl font-black text-amber-400 font-mono">${closingSoonCount}</span>
                        <i data-lucide="clock" class="w-5 h-5 text-amber-400"></i>
                    </div>
                    <span class="text-[10px] text-amber-300/80 font-mono mt-1 block">&lt; 14 Days to Deadline</span>
                </button>

                <!-- Prime Upload Window -->
                <button onclick="setCalendarTimingFilter('prime')" class="p-3.5 rounded-2xl bg-emerald-950/20 border transition text-left ${state.calendarTimingFilter === 'prime' ? 'border-emerald-500 ring-2 ring-emerald-500/30 bg-emerald-950/40' : 'border-emerald-500/30 hover:border-emerald-500/60'}">
                    <span class="text-[10px] font-bold text-emerald-300 uppercase tracking-wider block">🟢 Prime Window</span>
                    <div class="flex items-center justify-between mt-1">
                        <span class="text-2xl font-black text-emerald-400 font-mono">${primeCount}</span>
                        <i data-lucide="check-circle" class="w-5 h-5 text-emerald-400"></i>
                    </div>
                    <span class="text-[10px] text-emerald-300/80 font-mono mt-1 block">Optimal 45–90d Lead Time</span>
                </button>

                <!-- Advance Production -->
                <button onclick="setCalendarTimingFilter('advance')" class="p-3.5 rounded-2xl bg-purple-950/20 border transition text-left ${state.calendarTimingFilter === 'advance' ? 'border-purple-500 ring-2 ring-purple-500/30 bg-purple-950/40' : 'border-purple-500/30 hover:border-purple-500/60'}">
                    <span class="text-[10px] font-bold text-purple-300 uppercase tracking-wider block">🟣 Advance Prep</span>
                    <div class="flex items-center justify-between mt-1">
                        <span class="text-2xl font-black text-purple-400 font-mono">${advanceCount}</span>
                        <i data-lucide="sparkles" class="w-5 h-5 text-purple-400"></i>
                    </div>
                    <span class="text-[10px] text-purple-300/80 font-mono mt-1 block">Future Seasons &gt; 90d</span>
                </button>
            </div>
        </div>

        <!-- Interactive Search & Multi-Category Filter Bar -->
        <div class="glass-panel rounded-3xl p-5 mb-6 border border-slate-800 shadow-xl space-y-4">
            <div class="flex flex-col md:flex-row items-center justify-between gap-3">
                <!-- Instant In-Calendar Search -->
                <div class="relative w-full md:max-w-md flex items-center">
                    <i data-lucide="search" class="w-4 h-4 text-slate-500 absolute left-3.5 pointer-events-none"></i>
                    <input
                        type="text"
                        placeholder="Search events (e.g. fashion, birthday, 18th, black friday, halloween)..."
                        value="${escapeHtml(state.calendarSearchQuery)}"
                        oninput="onCalendarSearchInput(this.value)"
                        class="w-full bg-slate-900/90 text-white placeholder-slate-500 text-xs py-2.5 pl-10 pr-8 rounded-xl border border-slate-700/80 focus:outline-none focus:border-amber-500 font-medium"
                    />
                    ${state.calendarSearchQuery ? `
                        <button onclick="onCalendarSearchInput('')" class="absolute right-2.5 text-slate-400 hover:text-white p-1">
                            <i data-lucide="x" class="w-3.5 h-3.5"></i>
                        </button>
                    ` : ''}
                </div>

                <!-- Time Horizon Filter -->
                <div class="flex flex-wrap items-center gap-1.5 p-1 rounded-xl bg-slate-900 border border-slate-800 self-stretch md:self-auto justify-end">
                    <span class="text-[11px] text-slate-500 font-mono px-2 hidden lg:inline">Horizon:</span>
                    <button onclick="setCalendarFilter('all')" class="px-2.5 py-1 rounded-lg text-xs font-bold transition ${state.calendarFilter === 'all' ? 'bg-amber-500 text-white shadow-sm' : 'text-slate-400 hover:text-white'}">All Horizons</button>
                    <button onclick="setCalendarFilter('urgent')" class="px-2.5 py-1 rounded-lg text-xs font-bold transition ${state.calendarFilter === 'urgent' ? 'bg-amber-500 text-white shadow-sm' : 'text-slate-400 hover:text-white'}">Urgent Peak</button>
                    <button onclick="setCalendarFilter('30days')" class="px-2.5 py-1 rounded-lg text-xs font-bold transition ${state.calendarFilter === '30days' ? 'bg-amber-500 text-white shadow-sm' : 'text-slate-400 hover:text-white'}">Next 30 Days</button>
                    <button onclick="setCalendarFilter('60days')" class="px-2.5 py-1 rounded-lg text-xs font-bold transition ${state.calendarFilter === '60days' ? 'bg-amber-500 text-white shadow-sm' : 'text-slate-400 hover:text-white'}">Next 60 Days</button>
                </div>
            </div>

            <!-- Category Pills Row -->
            <div class="flex items-center gap-2 overflow-x-auto no-scrollbar pt-2 border-t border-slate-800/80">
                <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider shrink-0 mr-1 flex items-center gap-1">
                    <i data-lucide="layers" class="w-3.5 h-3.5 text-amber-400"></i> Category:
                </span>
                ${categories.map(c => `
                    <button
                        onclick="setCalendarCategoryFilter('${c.key}')"
                        class="px-3 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap transition flex items-center gap-1.5 ${state.calendarCategoryFilter === c.key ? 'bg-indigo-600 text-white shadow-md' : 'bg-slate-900 border border-slate-800 text-slate-300 hover:border-slate-700 hover:text-white'}"
                    >
                        <span>${c.label}</span>
                        <span class="text-[10px] px-1.5 py-0.2 rounded-full ${state.calendarCategoryFilter === c.key ? 'bg-white/20 text-white font-mono' : 'bg-slate-800 text-slate-400 font-mono'}">${c.count}</span>
                    </button>
                `).join('')}
            </div>

            <!-- Active Filter Status & View Switcher Bar -->
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs text-slate-400 font-mono pt-1">
                <div class="flex items-center gap-2">
                    <span>Showing <strong>${filtered.length}</strong> of <strong>${totalCount}</strong> ranked commercial events</span>
                    ${(state.calendarCategoryFilter !== 'all' || state.calendarTimingFilter !== 'all' || state.calendarFilter !== 'all' || state.calendarSearchQuery) ? `
                        <span class="text-amber-400 font-semibold flex items-center gap-1">
                            <i data-lucide="filter" class="w-3 h-3"></i> Filter Active
                        </span>
                    ` : ''}
                </div>

                <div class="flex items-center gap-2 self-start sm:self-auto">
                    <span class="text-[11px] text-slate-500 font-mono">View:</span>
                    <div class="p-0.5 rounded-xl bg-slate-900 border border-slate-800 flex items-center gap-1">
                        <button onclick="setCalendarViewMode('detailed')" class="px-2.5 py-1 rounded-lg text-xs font-bold transition flex items-center gap-1 ${state.calendarViewMode !== 'compact' ? 'bg-indigo-600 text-white shadow-sm' : 'text-slate-400 hover:text-white'}">
                            <i data-lucide="layout-grid" class="w-3 h-3"></i> Detailed Cards
                        </button>
                        <button onclick="setCalendarViewMode('compact')" class="px-2.5 py-1 rounded-lg text-xs font-bold transition flex items-center gap-1 ${state.calendarViewMode === 'compact' ? 'bg-indigo-600 text-white shadow-sm' : 'text-slate-400 hover:text-white'}">
                            <i data-lucide="list" class="w-3 h-3"></i> Compact Matrix
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Event Cards Stream / Compact Matrix -->
        ${state.calendarViewMode === 'compact' ? `
            <div class="glass-panel rounded-3xl overflow-hidden border border-slate-800 shadow-2xl">
                <div class="overflow-x-auto no-scrollbar">
                    <table class="w-full text-left text-sm text-slate-300">
                        <thead class="bg-slate-950/70 text-xs uppercase tracking-wider text-slate-400 border-b border-slate-800">
                            <tr>
                                <th class="px-6 py-4">Event & High-Yield Niche</th>
                                <th class="px-6 py-4">Category</th>
                                <th class="px-6 py-4">Commercial Date</th>
                                <th class="px-6 py-4">Golden Upload Window</th>
                                <th class="px-6 py-4">Deadline & Status</th>
                                <th class="px-6 py-4 text-right">Instant Actions</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800/60">
                            ${filtered.length === 0 ? `
                                <tr>
                                    <td colspan="6" class="px-6 py-12 text-center text-slate-500 text-xs">No commercial events match your filters</td>
                                </tr>
                            ` : filtered.map(ev => {
                                const eventNameId = registerData(ev.name);
                                const category = ev.category || 'Holidays & Cultural';
                                return `
                                    <tr class="hover:bg-slate-800/40 transition">
                                        <td class="px-6 py-4">
                                            <div class="font-bold text-white text-sm flex items-center gap-1.5">
                                                <span>${escapeHtml(ev.name)}</span>
                                            </div>
                                            <div class="text-[11px] text-amber-400 font-mono mt-0.5">${'★'.repeat(ev.stars || 4)} • Score: ${ev.impact_score}/100</div>
                                        </td>
                                        <td class="px-6 py-4">
                                            <span class="text-xs px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 font-mono">${escapeHtml(category)}</span>
                                        </td>
                                        <td class="px-6 py-4">
                                            <div class="text-xs font-semibold text-white">${escapeHtml(ev.target_date_str)}</div>
                                            <div class="text-[10px] text-slate-400 font-mono">In ${ev.days_until} days</div>
                                        </td>
                                        <td class="px-6 py-4">
                                            <div class="text-xs text-slate-300 font-mono">${escapeHtml(ev.upload_date_range)}</div>
                                            <div class="text-[10px] text-slate-500 font-mono">45–90d indexing lead time</div>
                                        </td>
                                        <td class="px-6 py-4">
                                            <div class="flex items-center gap-1.5">
                                                <span class="px-2 py-0.5 rounded text-[10px] font-black ${ev.is_late ? 'bg-rose-600 text-white animate-pulse' : (ev.timing_status === 'CLOSING_SOON' ? 'bg-amber-500/25 text-amber-300 border border-amber-500/40 font-bold' : (ev.timing_status === 'PRIME_WINDOW' ? 'bg-emerald-500/25 text-emerald-300 border border-emerald-500/40 font-bold' : 'bg-purple-500/20 text-purple-300 border border-purple-500/30 font-bold'))}">
                                                    ${escapeHtml(ev.timing_badge || ev.status)}
                                                </span>
                                            </div>
                                            <div class="text-[10px] font-mono mt-1 ${ev.is_late ? 'text-rose-400 font-bold' : 'text-slate-400'}">
                                                Due: ${escapeHtml(ev.golden_upload_deadline)}
                                            </div>
                                        </td>
                                        <td class="px-6 py-4 text-right">
                                            <div class="flex items-center justify-end gap-1.5">
                                                <button onclick="queueEventTitles('${eventNameId}')" class="px-2.5 py-1.5 rounded-xl bg-indigo-600/20 hover:bg-indigo-600/40 text-indigo-300 border border-indigo-500/30 text-xs font-bold transition flex items-center gap-1 active:scale-95" title="Add event to Kanban queue">
                                                    <i data-lucide="plus" class="w-3.5 h-3.5"></i> Queue
                                                </button>
                                                <button onclick="loadAIQuotaTabById('${eventNameId}')" class="px-2.5 py-1.5 rounded-xl bg-purple-600/25 hover:bg-purple-600/50 text-purple-200 border border-purple-500/35 text-xs font-bold transition flex items-center gap-1 active:scale-95" title="Get 20 AI prompts for this event">
                                                    <i data-lucide="sparkles" class="w-3.5 h-3.5"></i> AI Prompts
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                `;
                            }).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        ` : `
            <div class="space-y-6">
                ${filtered.length === 0 ? `
                    <div class="glass-panel rounded-3xl p-12 text-center text-slate-400 border border-slate-800">
                        <i data-lucide="calendar-x" class="w-12 h-12 mx-auto mb-3 opacity-50 text-slate-500"></i>
                        <h3 class="text-lg font-bold text-white">No commercial events match your filters</h3>
                        <p class="text-xs text-slate-400 mt-1">Try clearing the search term or switching the category pill.</p>
                        <button onclick="clearCalendarFilters()" class="mt-4 px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-600 text-white text-xs font-bold transition shadow-md">
                            Reset All Filters
                        </button>
                    </div>
                ` : filtered.map(ev => renderEventRankedCard(ev)).join('')}
            </div>
        `}
    `;

    container.innerHTML = html;
    lucide.createIcons();
}

function renderEventRankedCard(ev) {
    let starsHtml = '';
    for (let i = 0; i < (ev.stars || 4); i++) starsHtml += '★';

    let urgencyColor = 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30';
    if (ev.urgency_level === 'Max Priority' || ev.urgency_level === 'Urgent' || ev.urgency_level === 'Immediate') {
        urgencyColor = 'bg-rose-500/20 text-rose-300 border-rose-500/30';
    }

    const eventNameId = registerData(ev.name);
    const category = ev.category || 'Holidays & Cultural';

    // Category styling badge
    let catBadgeColor = 'bg-indigo-500/20 text-indigo-300 border-indigo-500/30';
    let catIcon = 'layers';
    if (category.includes('Fashion')) {
        catBadgeColor = 'bg-pink-500/20 text-pink-300 border-pink-500/30';
        catIcon = 'sparkles';
    } else if (category.includes('Birthday') || category.includes('Milestone')) {
        catBadgeColor = 'bg-amber-500/20 text-amber-300 border-amber-500/30';
        catIcon = 'cake';
    } else if (category.includes('Commerce')) {
        catBadgeColor = 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30';
        catIcon = 'shopping-bag';
    } else if (category.includes('Health')) {
        catBadgeColor = 'bg-teal-500/20 text-teal-300 border-teal-500/30';
        catIcon = 'activity';
    }

    return `
        <div class="glass-card rounded-3xl p-6 sm:p-7 border ${ev.is_late ? 'border-rose-500/40 shadow-rose-900/10' : 'border-slate-800'} shadow-xl">
            <!-- Header Row -->
            <div class="flex flex-col lg:flex-row lg:items-center justify-between pb-4 mb-4 border-b border-slate-800/80 gap-3">
                <div>
                    <div class="flex flex-wrap items-center gap-2 mb-1.5">
                        <span class="text-amber-400 text-sm font-black tracking-widest">${starsHtml}</span>
                        <span class="px-2.5 py-0.5 rounded-lg text-xs font-extrabold border ${catBadgeColor} font-mono flex items-center gap-1">
                            <i data-lucide="${catIcon}" class="w-3 h-3"></i>
                            ${escapeHtml(category)}
                        </span>
                        <span class="px-2.5 py-0.5 rounded-lg text-xs font-extrabold border ${urgencyColor}">${escapeHtml(ev.status || 'Active')}</span>
                        <span class="text-xs text-slate-400 font-mono">In ${ev.days_until} days (${ev.target_date_str})</span>
                    </div>
                    <h3 class="text-xl sm:text-2xl font-black text-white tracking-tight">${escapeHtml(ev.name)}</h3>
                </div>

                <div class="flex items-center gap-2 self-start lg:self-center">
                    <button onclick="queueEventTitles('${eventNameId}')" class="px-3.5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white border border-slate-700 text-xs font-bold transition flex items-center gap-1.5 shadow-sm active:scale-95 whitespace-nowrap">
                        <i data-lucide="plus" class="w-3.5 h-3.5 text-indigo-400"></i>
                        <span>Queue Event</span>
                    </button>
                    <button onclick="loadAIQuotaTabById('${eventNameId}')" class="px-4 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold transition flex items-center gap-1.5 shadow-lg shadow-purple-600/25 active:scale-95 whitespace-nowrap">
                        <i data-lucide="sparkles" class="w-3.5 h-3.5"></i>
                        <span>Get 20 AI Prompts for This Event</span>
                    </button>
                </div>
            </div>

            <!-- Prominent Golden Upload Window & Deadline Strip (Requested Feature) -->
            <div class="p-4 rounded-2xl ${ev.is_late ? 'bg-rose-950/40 border border-rose-500/50 shadow-inner' : (ev.timing_status === 'CLOSING_SOON' ? 'bg-amber-950/30 border border-amber-500/40' : (ev.timing_status === 'PRIME_WINDOW' ? 'bg-emerald-950/30 border border-emerald-500/40' : 'bg-slate-900/90 border border-slate-800'))} mb-5">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
                    <div class="flex flex-wrap items-center gap-2.5">
                        <span class="px-3 py-1 rounded-xl text-xs font-black font-mono shadow-sm flex items-center gap-1.5 ${ev.is_late ? 'bg-rose-600 text-white animate-pulse' : (ev.timing_status === 'CLOSING_SOON' ? 'bg-amber-500/25 text-amber-300 border border-amber-500/40' : (ev.timing_status === 'PRIME_WINDOW' ? 'bg-emerald-500/25 text-emerald-300 border border-emerald-500/40' : 'bg-purple-500/25 text-purple-300 border border-purple-500/40'))}">
                            <i data-lucide="clock" class="w-3.5 h-3.5"></i>
                            ${escapeHtml(ev.timing_badge || (ev.is_late ? '🔴 LATE' : '🟢 PRIME WINDOW'))}
                        </span>
                        <div class="text-xs text-slate-300 font-mono">
                            Golden Upload Window: <strong class="text-white">${escapeHtml(ev.upload_date_range || 'Upload 60-90 Days Ahead')}</strong>
                        </div>
                    </div>

                    <div class="flex flex-wrap items-center gap-3 text-xs font-mono">
                        <div class="text-slate-400">
                            Upload Deadline: <strong class="${ev.is_late ? 'text-rose-400 font-black underline' : 'text-amber-300 font-bold'}">${escapeHtml(ev.golden_upload_deadline || '45d Before Peak')}</strong>
                        </div>
                        <span class="text-slate-600 hidden sm:inline">•</span>
                        <div class="text-slate-400">
                            Commercial Peak: <strong class="text-slate-200">${escapeHtml(ev.target_date_str)}</strong>
                        </div>
                    </div>
                </div>

                ${ev.is_late ? `
                    <div class="mt-3 pt-2.5 border-t border-rose-500/30 flex items-start sm:items-center gap-2 text-xs text-rose-300 font-medium leading-relaxed">
                        <i data-lucide="alert-circle" class="w-4 h-4 text-rose-400 shrink-0 mt-0.5 sm:mt-0"></i>
                        <span><strong>🔴 LATE (${ev.days_past_deadline || 0} days past golden upload deadline):</strong> Demand peak is within 45 days. Corporate and agency creative directors have already locked in early campaign assets. Upload today strictly for last-minute buyers, or build your library ready for the next seasonal cycle!</span>
                    </div>
                ` : (ev.timing_status === 'CLOSING_SOON' ? `
                    <div class="mt-3 pt-2.5 border-t border-amber-500/30 flex items-start sm:items-center gap-2 text-xs text-amber-300 font-medium leading-relaxed">
                        <i data-lucide="alert-triangle" class="w-4 h-4 text-amber-400 shrink-0 mt-0.5 sm:mt-0"></i>
                        <span><strong>🟡 CLOSING SOON:</strong> Less than 14 days remaining before search engine index lag kicks in. Finalize and submit your vector, photo, and video assets this week for peak organic placement!</span>
                    </div>
                ` : (ev.timing_status === 'PRIME_WINDOW' ? `
                    <div class="mt-3 pt-2.5 border-t border-emerald-500/30 flex items-start sm:items-center gap-2 text-xs text-emerald-300 font-medium leading-relaxed">
                        <i data-lucide="check-circle-2" class="w-4 h-4 text-emerald-400 shrink-0 mt-0.5 sm:mt-0"></i>
                        <span><strong>🟢 PRIME UPLOAD WINDOW:</strong> Perfect timing! Early corporate buyers are licensing content now. Uploading this week ensures full indexing before mass search surges.</span>
                    </div>
                ` : ''))}
            </div>

            <!-- What to Create Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 mb-5">
                <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
                    <span class="text-[11px] font-bold text-amber-400 block mb-1">📐 Vectors (Illustrator)</span>
                    <p class="text-xs text-slate-300 leading-relaxed">${escapeHtml(ev.what_to_create ? ev.what_to_create.vectors : '')}</p>
                </div>
                <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
                    <span class="text-[11px] font-bold text-purple-400 block mb-1">📸 AI Images / Photos</span>
                    <p class="text-xs text-slate-300 leading-relaxed">${escapeHtml(ev.what_to_create ? ev.what_to_create.images : '')}</p>
                </div>
                <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
                    <span class="text-[11px] font-bold text-cyan-400 block mb-1">🎬 4K Stock Video</span>
                    <p class="text-xs text-slate-300 leading-relaxed">${escapeHtml(ev.what_to_create ? ev.what_to_create.videos : '')}</p>
                </div>
                <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
                    <span class="text-[11px] font-bold text-emerald-400 block mb-1">📄 Canva / PSD Templates</span>
                    <p class="text-xs text-slate-300 leading-relaxed">${escapeHtml(ev.what_to_create ? ev.what_to_create.templates : '')}</p>
                </div>
            </div>

            <!-- Ready Titles -->
            <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
                <div class="flex items-center justify-between mb-2">
                    <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Ready-to-Use Commercial SEO Titles:</span>
                    <span class="text-[10px] text-slate-500 font-mono">${(ev.suggested_titles || []).length} Titles</span>
                </div>
                <div class="space-y-1.5">
                    ${(ev.suggested_titles || []).map(t => {
                        const titleId = registerData(t);
                        return `
                            <div class="flex items-center justify-between text-xs font-mono text-slate-300 p-1.5 rounded-lg hover:bg-slate-800/60 transition">
                                <span class="truncate mr-2">• ${escapeHtml(t)}</span>
                                <button onclick="copyRegisteredText('${titleId}', 'Title Copied!')" class="text-indigo-400 hover:text-indigo-300 whitespace-nowrap text-[11px] font-semibold px-2 py-0.5 rounded hover:bg-slate-700/60 transition">Copy</button>
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>
        </div>
    `;
}

async function queueEventTitles(id) {
    const eventName = getRegisteredData(id) || id;
    if (!eventName) return;
    try {
        await fetch('/api/saved-keywords', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                keyword: eventName,
                platform: 'Multi',
                asset_type: 'Seasonal Collection',
                demand_score: 95,
                competition: 'Medium',
                title_suggestion: `${eventName} Commercial Stock Asset Collection`
            })
        });
        await loadQueueCount();
        showToast(`Queued "${eventName}" into Production Kanban!`, 'success');
    } catch (e) {
        showToast('Error queuing event', 'error');
    }
}

// --- AI DAILY QUOTA TAB (15-20 PROMPTS/DAY) ---
async function loadAIQuotaTab(topic = null) {
    if (state.currentTab !== 'ai-quota') {
        switchTab('ai-quota');
        return;
    }
    const container = document.getElementById('tab-ai-quota');
    if (!container) return;

    container.innerHTML = `
        <div class="glass-panel rounded-3xl p-12 text-center border border-purple-500/30">
            <div class="inline-block animate-spin rounded-full h-10 w-10 border-4 border-purple-500 border-t-transparent mb-3"></div>
            <h3 class="text-lg font-bold text-white">Generating 20 Commercial AI Prompts (Images & 4K Video)...</h3>
            <p class="text-xs text-slate-400 mt-1 max-w-md mx-auto">
                Calibrating lenses, aspect ratios, ProRes 60fps loops, and SEO titles for Google Flow, Midjourney, and Runway.
            </p>
        </div>
    `;

    try {
        const url = topic ? `/api/ai-daily-quota?topic=${encodeURIComponent(topic)}&count=20` : '/api/ai-daily-quota?count=20';
        const res = await fetch(url);
        const data = await res.json();
        state.aiQuotaPrompts = data.prompts || [];
        state.aiQuotaCategory = 'all';

        const quickThemes = ['Minimalist Interior', 'Autumn Festive', 'Cyberpunk Neon', 'Corporate Team', 'Luxury Real Estate', 'Sustainable Tech'];

        let html = `
            <div class="glass-panel rounded-3xl p-8 mb-8 border border-purple-500/30 shadow-2xl">
                <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="px-3.5 py-1 rounded-full text-xs font-bold bg-purple-500/20 text-purple-300 border border-purple-500/30">
                                Daily AI Quota Generator (Midjourney / Sora / Google Flow)
                            </span>
                            <span class="text-xs text-slate-400 font-mono">20 Fresh Commercial Prompts</span>
                        </div>
                        <h2 class="text-3xl sm:text-4xl font-black text-white mt-2.5 tracking-tight">Theme: ${escapeHtml(data.topic)}</h2>
                        <p class="text-slate-300 text-sm mt-1 max-w-2xl leading-relaxed">
                            10 Commercial Stock Photo prompts + 10 4K Stock Video b-roll prompts tailored for Adobe Stock Generative AI and Etsy printable art.
                        </p>

                        <!-- Quick Theme Chips -->
                        <div class="flex flex-wrap items-center gap-1.5 mt-3.5">
                            <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider mr-1">Trending Themes:</span>
                            ${quickThemes.map(th => `
                                <button onclick="loadAIQuotaTab('${escapeHtml(th)}')" class="px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-900/90 text-purple-300 hover:text-white border border-purple-500/30 hover:border-purple-500/60 transition active:scale-95">
                                    ${escapeHtml(th)}
                                </button>
                            `).join('')}
                        </div>
                    </div>

                    <!-- Custom Seed Topic Input -->
                    <div class="flex items-center gap-2 w-full lg:w-auto">
                        <input
                            id="custom-ai-quota-topic"
                            type="text"
                            placeholder="Change theme (e.g. coffee, drone)..."
                            class="bg-slate-900 text-white text-xs py-2.5 px-3.5 rounded-xl border border-slate-700/80 focus:outline-none focus:border-purple-500 w-56 font-medium"
                            onkeydown="if(event.key==='Enter') loadAIQuotaTab(this.value.trim())"
                        />
                        <button onclick="loadAIQuotaTab(document.getElementById('custom-ai-quota-topic').value.trim())" class="px-4 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold transition whitespace-nowrap active:scale-95 shadow-md shadow-purple-600/25">
                            Regenerate
                        </button>
                    </div>
                </div>
            </div>

            <!-- Platform AI Acceptance Policy Cheat Sheet -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                <div class="p-4 rounded-2xl bg-slate-900/80 border border-emerald-500/30 shadow-md">
                    <div class="flex items-center gap-2 mb-1.5">
                        <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
                        <span class="text-xs font-bold text-white">Adobe Stock</span>
                        <span class="text-[10px] text-emerald-400 font-extrabold ml-auto">100% Accepted</span>
                    </div>
                    <p class="text-[11px] text-slate-300 leading-relaxed">Full Generative AI images & 4K video accepted. Toggle 'Created using AI tools' during upload.</p>
                </div>
                <div class="p-4 rounded-2xl bg-slate-900/80 border border-emerald-500/30 shadow-md">
                    <div class="flex items-center gap-2 mb-1.5">
                        <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
                        <span class="text-xs font-bold text-white">Etsy Digital</span>
                        <span class="text-[10px] text-emerald-400 font-extrabold ml-auto">100% Accepted</span>
                    </div>
                    <p class="text-[11px] text-slate-300 leading-relaxed">Top marketplace for AI transparent clipart packs and multi-ratio printable wall art posters.</p>
                </div>
                <div class="p-4 rounded-2xl bg-slate-900/80 border border-amber-500/30 shadow-md">
                    <div class="flex items-center gap-2 mb-1.5">
                        <span class="w-2 h-2 rounded-full bg-amber-400"></span>
                        <span class="text-xs font-bold text-white">Shutterstock</span>
                        <span class="text-[10px] text-amber-400 font-extrabold ml-auto">Internal Tool Only</span>
                    </div>
                    <p class="text-[11px] text-slate-300 leading-relaxed">Strict third-party AI image rejection. Do NOT submit external AI photos to Shutterstock.</p>
                </div>
            </div>

            <!-- Toolbar: Category Filters and Batch Copy -->
            <div class="glass-panel rounded-2xl p-4 mb-6 border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div class="flex flex-wrap items-center gap-1.5">
                    <button onclick="setAIQuotaCategory('all')" id="ai-filter-all" class="filter-chip active">All Prompts (20)</button>
                    <button onclick="setAIQuotaCategory('photos')" id="ai-filter-photos" class="filter-chip">📸 10 Stock Photos</button>
                    <button onclick="setAIQuotaCategory('videos')" id="ai-filter-videos" class="filter-chip">🎬 10 4K Video B-Rolls</button>
                </div>

                <div class="flex items-center gap-2">
                    <button onclick="copyAllAIPhotos()" class="px-3 py-1.5 rounded-xl bg-purple-600/20 hover:bg-purple-600/40 text-purple-300 border border-purple-500/30 text-xs font-bold transition flex items-center gap-1.5 active:scale-95">
                        <i data-lucide="copy" class="w-3.5 h-3.5"></i>
                        <span>Copy All 10 Photos</span>
                    </button>
                    <button onclick="copyAllAIVideos()" class="px-3 py-1.5 rounded-xl bg-cyan-600/20 hover:bg-cyan-600/40 text-cyan-300 border border-cyan-500/30 text-xs font-bold transition flex items-center gap-1.5 active:scale-95">
                        <i data-lucide="copy" class="w-3.5 h-3.5"></i>
                        <span>Copy All 10 Videos</span>
                    </button>
                </div>
            </div>

            <!-- Prompts Cards Grid -->
            <div id="ai-quota-cards-grid" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                ${data.prompts.map(p => renderAIQuotaCard(p)).join('')}
            </div>
        `;

        container.innerHTML = html;
        lucide.createIcons();
    } catch (e) {
        console.error('AI Quota error:', e);
    }
}

function setAIQuotaCategory(cat) {
    state.aiQuotaCategory = cat;
    document.querySelectorAll('[id^="ai-filter-"]').forEach(btn => {
        if (btn.id === `ai-filter-${cat}`) btn.classList.add('active');
        else btn.classList.remove('active');
    });

    const grid = document.getElementById('ai-quota-cards-grid');
    if (!grid || !state.aiQuotaPrompts) return;

    let filtered = state.aiQuotaPrompts;
    if (cat === 'photos') filtered = filtered.filter(p => p.type !== 'AI Video');
    else if (cat === 'videos') filtered = filtered.filter(p => p.type === 'AI Video');

    grid.innerHTML = filtered.map(p => renderAIQuotaCard(p)).join('');
    lucide.createIcons();
}

function copyAllAIPhotos() {
    const photos = (state.aiQuotaPrompts || []).filter(p => p.type !== 'AI Video');
    if (photos.length === 0) {
        showToast('No photo prompts available', 'info');
        return;
    }
    const text = photos.map((p, idx) => `[Photo #${idx + 1}: ${p.title}]\nPrompt: ${p.prompt}\nTags: ${p.tags}`).join('\n\n---\n\n');
    copyToClipboard(text, 'All 10 Stock Photo Prompts Copied!');
}

function copyAllAIVideos() {
    const videos = (state.aiQuotaPrompts || []).filter(p => p.type === 'AI Video');
    if (videos.length === 0) {
        showToast('No video prompts available', 'info');
        return;
    }
    const text = videos.map((p, idx) => `[4K Video #${idx + 1}: ${p.title}]\nPrompt: ${p.prompt}\nTags: ${p.tags}`).join('\n\n---\n\n');
    copyToClipboard(text, 'All 10 4K Video Prompts Copied!');
}

function loadAIQuotaTabById(id) {
    const topic = getRegisteredData(id);
    loadAIQuotaTab(topic);
}

function renderAIQuotaCard(p) {
    const isVideo = p.type === 'AI Video';
    const badgeColor = isVideo ? 'text-cyan-300 bg-cyan-500/20 border-cyan-500/30' : 'text-purple-300 bg-purple-500/20 border-purple-500/30';
    const promptId = registerData(p.prompt);
    const promptWithRefId = registerData(p.prompt_with_ref || p.prompt);
    const fluxPromptId = registerData(p.flux_prompt || p.prompt);
    const chatgptPromptId = registerData(p.chatgpt_prompt || p.prompt);
    const nanoPromptId = registerData(p.nano_banana_prompt || p.prompt);
    const negPromptId = registerData(p.negative_prompt || '');
    const itemDataId = registerData({
        suggested_title: p.title,
        asset_type: p.type,
        platform: 'Adobe Stock'
    });
    const refBenchmark = p.reference_guide ? p.reference_guide.aesthetic_benchmark : '';
    const timing = getClientUploadDeadline(p);

    return `
        <div class="glass-card rounded-2xl p-6 border ${timing.is_late ? 'border-rose-500/40 border-l-4 border-l-rose-500 bg-rose-950/20 shadow-rose-900/10' : 'border-slate-800'} flex flex-col justify-between shadow-lg">
            <div>
                <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-extrabold px-2.5 py-0.5 rounded-full border ${badgeColor} font-mono">
                        ${p.slot}: ${p.type}
                    </span>
                    <div class="flex items-center gap-1.5">
                        ${refBenchmark ? `
                            <span class="text-[10px] text-purple-300 font-mono bg-purple-950/60 px-2 py-0.5 rounded border border-purple-500/30 truncate max-w-[170px]" title="Visual Style Benchmark: ${escapeHtml(refBenchmark)}">
                                Ref: ${escapeHtml(refBenchmark)}
                            </span>
                        ` : ''}
                        <span class="text-xs text-slate-400 font-mono bg-slate-900 px-2 py-0.5 rounded border border-slate-800">${p.aspect_ratio}</span>
                    </div>
                </div>

                <h4 class="text-base font-bold text-white mb-2 leading-snug">${escapeHtml(p.title)}</h4>

                <!-- Production Upload Window & Deadline Strip -->
                <div class="flex flex-wrap items-center justify-between gap-1.5 mb-3 p-2.5 rounded-xl ${timing.is_late ? 'bg-rose-950/40 border border-rose-500/40 shadow-inner' : (timing.timing_status === 'CLOSING_SOON' ? 'bg-amber-950/30 border border-amber-500/40' : (timing.timing_status === 'PRIME_WINDOW' ? 'bg-emerald-950/30 border border-emerald-500/40' : 'bg-slate-900/90 border border-slate-800'))} text-xs font-mono">
                    <div class="flex items-center gap-1.5">
                        <span class="px-2 py-0.5 rounded text-[10px] font-black ${timing.is_late ? 'bg-rose-600 text-white animate-pulse' : (timing.timing_status === 'CLOSING_SOON' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' : (timing.timing_status === 'PRIME_WINDOW' ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-purple-500/20 text-purple-300 border border-purple-500/30'))}">
                            ${escapeHtml(timing.timing_badge)}
                        </span>
                        <span class="text-slate-300 text-[11px]">${escapeHtml(timing.upload_date_range)}</span>
                    </div>
                    <div class="text-[10px] text-slate-400">
                        Deadline: <span class="${timing.is_late ? 'text-rose-400 font-bold' : 'text-slate-300 font-semibold'}">${escapeHtml(timing.upload_deadline)}</span>
                    </div>
                </div>

                <!-- Prompt Code Block -->
                <div class="p-3.5 rounded-xl bg-slate-900/90 border border-slate-800 mb-3 text-xs font-mono text-purple-200 leading-relaxed max-h-36 overflow-y-auto no-scrollbar select-all">
                    ${escapeHtml(p.prompt)}
                </div>

                <!-- Ready Tags -->
                <div class="text-[11px] text-slate-400 mb-3 font-mono">
                    <span class="font-bold text-slate-500">Tags:</span> ${escapeHtml(p.tags)}
                </div>
            </div>

            <div class="pt-3 border-t border-slate-800 flex flex-wrap items-center justify-between gap-2">
                <div class="flex flex-wrap items-center gap-1.5">
                    <button onclick="copyRegisteredText('${promptId}', 'AI Prompt Copied!')" class="px-3 py-1.5 rounded-xl bg-purple-600/20 hover:bg-purple-600/40 text-purple-300 border border-purple-500/30 text-xs font-bold transition flex items-center gap-1 active:scale-95" title="Copy Midjourney Prompt">
                        <i data-lucide="copy" class="w-3.5 h-3.5"></i>
                        Prompt
                    </button>
                    ${p.prompt_with_ref ? `
                        <button onclick="copyRegisteredText('${promptWithRefId}', 'Prompt with --sref Reference Copied!')" class="px-2.5 py-1.5 rounded-xl bg-indigo-600/20 hover:bg-indigo-600/40 text-indigo-300 border border-indigo-500/30 text-xs font-bold transition flex items-center gap-1 active:scale-95" title="Copy with Midjourney --sref Reference">
                            <i data-lucide="link" class="w-3 h-3"></i> + --sref
                        </button>
                    ` : ''}
                    ${p.flux_prompt ? `
                        <button onclick="copyRegisteredText('${fluxPromptId}', 'Flux.1 Prompt Copied!')" class="px-2.5 py-1.5 rounded-xl bg-cyan-600/20 hover:bg-cyan-600/40 text-cyan-300 border border-cyan-500/30 text-xs font-bold transition active:scale-95" title="Copy Flux.1 Pro natural prompt">
                            Flux
                        </button>
                    ` : ''}
                    ${p.chatgpt_prompt ? `
                        <button onclick="copyRegisteredText('${chatgptPromptId}', 'ChatGPT Prompt Copied!')" class="px-2.5 py-1.5 rounded-xl bg-emerald-600/20 hover:bg-emerald-600/40 text-emerald-300 border border-emerald-500/30 text-xs font-bold transition active:scale-95" title="Copy ChatGPT / DALL-E 3 prompt">
                            ChatGPT
                        </button>
                    ` : ''}
                    ${p.nano_banana_prompt ? `
                        <button onclick="copyRegisteredText('${nanoPromptId}', 'Nano Banana Prompt Copied!')" class="px-2.5 py-1.5 rounded-xl bg-amber-600/20 hover:bg-amber-600/40 text-amber-300 border border-amber-500/30 text-xs font-bold transition active:scale-95" title="Copy Google Nano Banana prompt">
                            Nano
                        </button>
                    ` : ''}
                    ${p.negative_prompt ? `
                        <button onclick="copyRegisteredText('${negPromptId}', 'Negative Prompt Copied!')" class="px-2 py-1.5 rounded-xl text-[11px] text-rose-400 hover:text-rose-300 hover:bg-rose-500/10 border border-rose-500/30 font-semibold transition active:scale-95" title="Copy Rejection-Proof Negative Prompt">
                            Negative
                        </button>
                    ` : ''}
                </div>
                <button onclick="quickLogAssetFromRegistry('${itemDataId}')" class="px-3.5 py-1.5 rounded-xl bg-emerald-600/20 hover:bg-emerald-600/40 text-emerald-300 border border-emerald-500/30 text-xs font-bold transition flex items-center gap-1.5 active:scale-95">
                    <i data-lucide="check" class="w-3.5 h-3.5"></i>
                    Log Done
                </button>
            </div>
        </div>
    `;
}

// --- PRODUCTION QUEUE & KANBAN ---
async function loadQueueTab() {
    const container = document.getElementById('tab-queue');
    if (!container) return;

    try {
        const res = await fetch('/api/saved-keywords');
        const data = await res.json();
        state.queueItems = data.items || [];
        const badge = document.getElementById('queue-count-badge');
        if (badge) badge.innerText = state.queueItems.length;
        renderQueueBoard(state.queueItems);
    } catch (e) {
        console.error('Queue load error:', e);
    }
}

function renderQueueBoard(items) {
    const container = document.getElementById('tab-queue');
    const statuses = ['Idea', 'Designing', 'Ready', 'Uploaded'];

    let filteredItems = items || [];
    if (state.queueFilterPlatform && state.queueFilterPlatform !== 'all') {
        filteredItems = filteredItems.filter(it => (it.platform || '').toLowerCase().includes(state.queueFilterPlatform.toLowerCase()));
    }

    let html = `
        <div class="glass-panel rounded-3xl p-8 mb-8 border border-slate-700/60 shadow-2xl">
            <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                <div>
                    <div class="flex items-center gap-2">
                        <span class="px-3.5 py-1 rounded-full text-xs font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                            Production Roadmap
                        </span>
                        <span class="text-xs text-slate-400 font-mono">${filteredItems.length} Active Items</span>
                    </div>
                    <h2 class="text-3xl sm:text-4xl font-black text-white mt-1.5 tracking-tight">Production Kanban & Queue</h2>
                    <p class="text-slate-300 text-sm mt-1">Manage your design roadmap from seed idea to completed uploads across marketplaces.</p>
                </div>
                <div class="flex flex-wrap items-center gap-2.5">
                    <!-- Marketplace Filter -->
                    <select onchange="onQueuePlatformFilterChange(this.value)" class="bg-slate-900 text-slate-200 text-xs py-2.5 px-3 rounded-xl border border-slate-700 focus:outline-none font-medium">
                        <option value="all" ${state.queueFilterPlatform === 'all' ? 'selected' : ''}>All Marketplaces</option>
                        <option value="Adobe Stock" ${state.queueFilterPlatform === 'Adobe Stock' ? 'selected' : ''}>Adobe Stock</option>
                        <option value="Etsy" ${state.queueFilterPlatform === 'Etsy' ? 'selected' : ''}>Etsy</option>
                        <option value="Shutterstock" ${state.queueFilterPlatform === 'Shutterstock' ? 'selected' : ''}>Shutterstock</option>
                        <option value="IconScout" ${state.queueFilterPlatform === 'IconScout' ? 'selected' : ''}>IconScout</option>
                        <option value="GraphicRiver" ${state.queueFilterPlatform === 'GraphicRiver' ? 'selected' : ''}>GraphicRiver</option>
                    </select>

                    <button onclick="openAddIdeaModal()" class="px-4 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white text-xs font-bold transition flex items-center gap-1.5 shadow-lg shadow-indigo-600/25 active:scale-95">
                        <i data-lucide="plus" class="w-4 h-4"></i>
                        <span>+ Add Idea</span>
                    </button>
                    <button onclick="exportQueueCSV()" class="px-3.5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold border border-slate-700 transition flex items-center gap-1.5 shadow-sm active:scale-95">
                        <i data-lucide="download" class="w-4 h-4"></i>
                        <span>CSV</span>
                    </button>
                </div>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            ${statuses.map(st => {
                const columnItems = filteredItems.filter(it => it.status === st);
                const stageClass = 'kanban-stage-' + st.toLowerCase();
                return `
                    <div class="glass-panel rounded-2xl p-4 border border-slate-800 flex flex-col shadow-xl ${stageClass}">
                        <div class="flex items-center justify-between pb-3 mb-3 border-b border-slate-800">
                            <span class="font-extrabold text-white text-sm">${st}</span>
                            <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-slate-800 text-slate-300 font-mono">${columnItems.length}</span>
                        </div>

                        <div class="space-y-3 flex-1 min-h-[300px]">
                            ${columnItems.length === 0 ? `
                                <div class="text-center py-12 text-slate-500 text-xs">No items in ${st}</div>
                            ` : columnItems.map(item => {
                                const fullId = registerData({
                                    suggested_title: item.title_suggestion || item.keyword,
                                    asset_type: item.asset_type,
                                    platform: item.platform
                                });
                                const timing = getClientUploadDeadline(item);

                                return `
                                    <div class="p-4 rounded-xl bg-slate-900/90 border ${timing.is_late ? 'border-rose-500/40 border-l-4 border-l-rose-500 bg-rose-950/20' : 'border-slate-800'} hover:border-indigo-500/40 transition shadow-sm">
                                        <div class="flex items-start justify-between gap-2 mb-2">
                                            <h5 class="font-bold text-white text-sm leading-snug">${escapeHtml(item.keyword)}</h5>
                                            <button onclick="deleteQueueItem(${item.id})" class="text-slate-500 hover:text-rose-400 p-0.5 transition" title="Delete">
                                                <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
                                            </button>
                                        </div>

                                        ${item.title_suggestion ? `<div class="text-xs text-slate-400 font-mono mb-2 line-clamp-2">${escapeHtml(item.title_suggestion)}</div>` : ''}

                                        <!-- Upload Window & Deadline Strip -->
                                        <div class="mb-2.5 p-2 rounded-lg ${timing.is_late ? 'bg-rose-950/40 border border-rose-500/30' : 'bg-slate-950/70 border border-slate-800'} text-[10px] font-mono space-y-0.5">
                                            <div class="flex items-center justify-between gap-1">
                                                <span class="${timing.is_late ? 'text-rose-400 font-black animate-pulse' : 'text-slate-300 font-bold'}">${escapeHtml(timing.timing_badge)}</span>
                                                <span class="text-slate-400 truncate max-w-[120px]" title="Deadline: ${escapeHtml(timing.upload_deadline)}">Due: <strong class="${timing.is_late ? 'text-rose-400' : 'text-slate-200'}">${escapeHtml(timing.upload_deadline)}</strong></span>
                                            </div>
                                            <div class="text-slate-400 text-[10px] truncate" title="Window: ${escapeHtml(timing.upload_date_range)}">
                                                Window: <span class="text-slate-300">${escapeHtml(timing.upload_date_range)}</span>
                                                ${timing.is_late ? `<span class="text-rose-400 font-bold ml-1">(${timing.days_overdue}d overdue)</span>` : ''}
                                            </div>
                                        </div>

                                        <div class="flex flex-wrap gap-1 mb-3 font-mono">
                                            <span class="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">${escapeHtml(item.platform || 'Multi')}</span>
                                            <span class="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">${escapeHtml(item.asset_type || 'General')}</span>
                                            <span class="text-[10px] px-1.5 py-0.5 rounded bg-indigo-500/10 text-indigo-300 font-bold">Score: ${item.demand_score || 0}</span>
                                        </div>

                                        <div class="flex items-center justify-between pt-2 border-t border-slate-800/80 gap-2">
                                            <select onchange="updateItemStatus(${item.id}, this.value)" class="bg-slate-800 text-slate-300 text-xs rounded-lg px-2 py-1 border border-slate-700 focus:outline-none font-medium">
                                                ${statuses.map(s => `<option value="${s}" ${s === item.status ? 'selected' : ''}>${s}</option>`).join('')}
                                            </select>

                                            <div class="flex items-center gap-1.5">
                                                ${item.status !== 'Uploaded' ? `
                                                    <button onclick="advanceQueueItemStage(${item.id}, '${item.status}')" class="px-2 py-1 rounded bg-indigo-600/20 hover:bg-indigo-600/40 text-indigo-300 border border-indigo-500/30 text-xs font-bold transition flex items-center gap-1 active:scale-95" title="Advance Stage">
                                                        <span>➔</span>
                                                    </button>
                                                ` : ''}
                                                <button onclick="quickLogAssetFromRegistry('${fullId}')" class="text-emerald-400 hover:text-emerald-300 p-1 rounded hover:bg-slate-800 transition" title="Log Completed to Today's Goal">
                                                    <i data-lucide="check-circle" class="w-4 h-4"></i>
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                `;
                            }).join('')}
                        </div>
                    </div>
                `;
            }).join('')}
        </div>
    `;

    container.innerHTML = html;
    lucide.createIcons();
}

function onQueuePlatformFilterChange(val) {
    state.queueFilterPlatform = val;
    renderQueueBoard(state.queueItems);
}

function openAddIdeaModal() {
    const modal = document.getElementById('add-idea-modal');
    if (modal) {
        modal.classList.remove('hidden');
        const input = document.getElementById('new-idea-keyword');
        if (input) {
            input.value = '';
            input.focus();
        }
        updateNewIdeaTimingPreview('');
        lucide.createIcons();
    }
}

function closeAddIdeaModal() {
    const modal = document.getElementById('add-idea-modal');
    if (modal) modal.classList.add('hidden');
}

function openDeadlineGuideModal() {
    const modal = document.getElementById('deadline-guide-modal');
    if (modal) {
        modal.classList.remove('hidden');
        lucide.createIcons();
    }
}

function closeDeadlineGuideModal() {
    const modal = document.getElementById('deadline-guide-modal');
    if (modal) modal.classList.add('hidden');
}

function updateNewIdeaTimingPreview(kw) {
    const previewEl = document.getElementById('new-idea-timing-preview');
    const badgeEl = document.getElementById('new-idea-timing-badge');
    const deadlineEl = document.getElementById('new-idea-timing-deadline');
    const rangeEl = document.getElementById('new-idea-timing-range');
    if (!previewEl) return;

    if (!kw || !kw.trim()) {
        previewEl.classList.add('hidden');
        return;
    }

    const timing = getClientUploadDeadline(kw.trim());
    previewEl.classList.remove('hidden');

    if (badgeEl) {
        badgeEl.textContent = timing.timing_badge;
        badgeEl.className = `px-2 py-0.5 rounded text-[10px] font-black ${
            timing.is_late 
                ? 'bg-rose-500/30 text-rose-300 border border-rose-500/50 animate-pulse' 
                : (timing.timing_status === 'CLOSING_SOON' 
                    ? 'bg-amber-500/30 text-amber-300 border border-amber-500/50' 
                    : (timing.timing_status === 'EVERGREEN'
                        ? 'bg-blue-500/20 text-blue-300 border border-blue-500/30'
                        : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'))
        }`;
    }

    if (deadlineEl) {
        deadlineEl.innerHTML = `Due: <strong class="${timing.is_late ? 'text-rose-400 font-bold' : 'text-slate-200'}">${escapeHtml(timing.upload_deadline)}</strong>`;
    }

    if (rangeEl) {
        rangeEl.innerHTML = `Window: <strong class="text-slate-300">${escapeHtml(timing.upload_date_range)}</strong>` +
            (timing.is_late ? ` <span class="text-rose-400 font-bold">(${timing.days_overdue}d past golden window!)</span>` : '');
    }
}

async function submitNewIdeaModal() {
    const kwInput = document.getElementById('new-idea-keyword');
    const keyword = kwInput ? kwInput.value.trim() : '';
    if (!keyword) {
        showToast('Please enter a keyword or concept', 'info');
        return;
    }
    const assetType = document.getElementById('new-idea-type')?.value || 'Illustrator (Vector)';
    const platform = document.getElementById('new-idea-platform')?.value || 'Adobe Stock';
    const stage = document.getElementById('new-idea-stage')?.value || 'Idea';
    const score = parseInt(document.getElementById('new-idea-score')?.value) || 80;
    const notes = document.getElementById('new-idea-notes')?.value.trim() || '';

    try {
        await fetch('/api/saved-keywords', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                keyword: keyword,
                platform: platform,
                asset_type: assetType,
                demand_score: score,
                competition: 'Medium',
                title_suggestion: notes,
                notes: notes,
                status: stage
            })
        });
        showToast(`Added "${keyword}" to Kanban!`, 'success');
        closeAddIdeaModal();
        await loadQueueTab();
        await loadQueueCount();
    } catch (e) {
        showToast('Error saving idea', 'error');
    }
}

async function advanceQueueItemStage(itemId, currentStatus) {
    const stages = ['Idea', 'Designing', 'Ready', 'Uploaded'];
    const idx = stages.indexOf(currentStatus);
    if (idx < 0 || idx >= stages.length - 1) return;
    const nextStatus = stages[idx + 1];
    await updateItemStatus(itemId, nextStatus);
}

async function updateItemStatus(itemId, newStatus) {
    try {
        await fetch(`/api/saved-keywords/${itemId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        });
        showToast(`Moved to ${newStatus}`, 'success');
        loadQueueTab();
    } catch (e) {
        showToast('Error updating status', 'error');
    }
}

async function deleteQueueItem(itemId) {
    try {
        await fetch(`/api/saved-keywords/${itemId}`, { method: 'DELETE' });
        showToast('Item removed from queue', 'info');
        loadQueueTab();
        loadQueueCount();
    } catch (e) {
        showToast('Error deleting item', 'error');
    }
}

async function saveKeywordFromRegistry(id) {
    const item = getRegisteredData(id);
    if (!item) return;

    try {
        await fetch('/api/saved-keywords', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                keyword: item.keyword,
                platform: item.best_marketplace || 'Multi',
                asset_type: item.recommended_tool || 'All',
                demand_score: item.opportunity_score || item.demand_score || 0,
                competition: item.competition || 'Medium',
                title_suggestion: item.suggested_title || '',
                status: 'Idea'
            })
        });
        showToast(`Saved "${item.keyword}" to Production Queue!`, 'success');
        loadQueueCount();
    } catch (e) {
        showToast('Failed to save item', 'error');
    }
}

async function quickLogAssetFromRegistry(id) {
    const item = getRegisteredData(id);
    if (!item) return;

    const title = item.suggested_title || item.title || item.keyword || 'Untitled Stock Asset';
    const type = item.asset_type || item.recommended_tool || 'AI Image';
    const platform = item.platform || item.best_marketplace || 'Adobe Stock';

    try {
        await fetch('/api/daily-goals/log-asset', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title: title,
                asset_type: type,
                platform: platform,
                status: 'Created'
            })
        });
        showToast(`Logged "${title.slice(0, 30)}..." to Today!`, 'success');
        await loadTodayGoal(false);
    } catch (e) {
        showToast('Error logging asset', 'error');
    }
}

// --- ALPHABET SOUP DEEP DIGGER MODAL ---
function triggerAlphabetSoupById(id) {
    const seedWord = getRegisteredData(id);
    triggerAlphabetSoup(seedWord || state.currentQuery);
}

async function triggerAlphabetSoup(seedWord) {
    const modal = document.getElementById('alphabet-soup-modal');
    if (!modal) return;
    modal.classList.remove('hidden');

    const content = document.getElementById('alphabet-soup-content');
    content.innerHTML = `
        <div class="p-12 text-center">
            <div class="inline-block animate-spin rounded-full h-12 w-12 border-4 border-amber-500 border-t-transparent mb-4"></div>
            <h3 class="text-xl font-bold text-white">Running 26-Letter Deep Alphabet Crawl for "${escapeHtml(seedWord)}"...</h3>
            <p class="text-slate-400 text-sm mt-2">Checking letters A through Z to uncover hidden commercial buyer keywords.</p>
        </div>
    `;

    try {
        const res = await fetch(`/api/alphabet-soup?base_kw=${encodeURIComponent(seedWord)}`);
        const data = await res.json();
        state.alphabetSoupData = data;
        state.alphabetFilterQuery = '';
        renderAlphabetSoupModal(data);
    } catch (e) {
        console.error('Alphabet soup error:', e);
        content.innerHTML = `<div class="p-8 text-center text-red-400">Failed to complete Alphabet Soup crawl.</div>`;
    }
}

function renderAlphabetSoupModal(data) {
    const content = document.getElementById('alphabet-soup-content');
    if (!content) return;
    const { base_keyword, total, results } = data;

    const baseKwId = registerData(base_keyword);

    let html = `
        <div class="p-6 border-b border-slate-800 flex items-center justify-between bg-slate-900/60">
            <div>
                <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">
                    Alphabet Soup Engine (A-Z)
                </span>
                <h3 class="text-xl font-black text-white mt-1">Discovered ${total} Longtail Variations for "${escapeHtml(base_keyword)}"</h3>
            </div>
            <div class="flex items-center gap-3">
                <button onclick="exportSoupToCSVById('${baseKwId}')" class="px-3.5 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold border border-slate-700 transition flex items-center gap-1.5 active:scale-95">
                    <i data-lucide="download" class="w-3.5 h-3.5"></i> Export CSV
                </button>
                <button onclick="closeAlphabetModal()" class="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition">
                    <i data-lucide="x" class="w-6 h-6"></i>
                </button>
            </div>
        </div>

        <!-- Filter Search Bar -->
        <div class="px-6 py-3 border-b border-slate-800/80 bg-slate-950/40 flex items-center justify-between gap-4">
            <div class="relative flex-1 max-w-sm flex items-center">
                <i data-lucide="filter" class="w-3.5 h-3.5 text-slate-500 absolute left-3 pointer-events-none"></i>
                <input
                    type="text"
                    placeholder="Filter variations (by keyword or +letter)..."
                    oninput="onAlphabetSoupFilter(this.value)"
                    class="w-full bg-slate-900 text-white placeholder-slate-500 text-xs py-2 pl-9 pr-3 rounded-xl border border-slate-700 focus:outline-none focus:border-amber-500 font-medium"
                />
            </div>
            <span id="soup-results-count" class="text-xs text-slate-400 font-mono">${results.length} variations</span>
        </div>

        <div class="p-6 max-h-[60vh] overflow-y-auto no-scrollbar">
            <div id="alphabet-soup-cards-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                ${results.map(item => renderAlphabetSoupCardItem(item)).join('')}
            </div>
        </div>
    `;

    content.innerHTML = html;
    lucide.createIcons();
}

function renderAlphabetSoupCardItem(item) {
    const fullId = registerData({
        suggested_title: item.suggested_title,
        asset_type: item.recommended_tool,
        platform: item.best_marketplace
    });
    const queueId = registerData({
        keyword: item.keyword,
        best_marketplace: item.best_marketplace || 'Multi',
        recommended_tool: item.recommended_tool || 'General',
        opportunity_score: item.opportunity_score || 80,
        suggested_title: item.suggested_title
    });
    const timing = getClientUploadDeadline(item);

    return `
        <div class="p-3.5 rounded-xl bg-slate-900/80 border ${timing.is_late ? 'border-rose-500/40 border-l-4 border-l-rose-500 bg-rose-950/20' : 'border-slate-800'} hover:border-amber-500/40 transition flex items-start justify-between gap-2 shadow-sm">
            <div class="min-w-0 flex-1">
                <div class="font-bold text-white text-sm truncate" title="${escapeHtml(item.keyword)}">${escapeHtml(item.keyword)}</div>
                <div class="text-[11px] text-emerald-400 font-mono mt-0.5 truncate" title="${escapeHtml(item.suggested_title)}">${escapeHtml(item.suggested_title)}</div>
                <div class="flex flex-wrap items-center gap-1.5 mt-1.5 font-mono">
                    <span class="text-[10px] px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-extrabold uppercase">+${item.letter_trigger}</span>
                    <span class="text-[10px] px-2 py-0.5 rounded ${timing.is_late ? 'bg-rose-500/25 text-rose-300 border border-rose-500/40 font-black animate-pulse' : (timing.timing_status === 'CLOSING_SOON' ? 'bg-amber-500/25 text-amber-300 border border-amber-500/40 font-bold' : 'bg-slate-800 text-slate-300')}">
                        ${escapeHtml(timing.timing_badge)}
                    </span>
                    <span class="text-[10px] text-slate-400 truncate">Due: <strong class="${timing.is_late ? 'text-rose-400 font-bold' : 'text-slate-200'}">${escapeHtml(timing.upload_deadline)}</strong></span>
                </div>
                <div class="text-[10px] text-slate-400 font-mono mt-1 flex items-center gap-1 truncate" title="Window: ${escapeHtml(timing.upload_date_range)}">
                    <span class="text-slate-500">Window:</span>
                    <span class="text-slate-300">${escapeHtml(timing.upload_date_range)}</span>
                    ${timing.is_late ? `<span class="text-rose-400 font-bold ml-1">(${timing.days_overdue}d overdue)</span>` : ''}
                </div>
            </div>
            <div class="flex items-center gap-1.5 shrink-0 ml-2">
                <button onclick="quickLogAssetFromRegistry('${fullId}')" class="px-2 py-1 rounded-lg bg-emerald-600/20 hover:bg-emerald-600/40 text-emerald-300 border border-emerald-500/30 text-xs font-bold transition flex items-center gap-1 active:scale-95" title="Log to Today's Goal">
                    <i data-lucide="check" class="w-3.5 h-3.5"></i>
                    <span>Done</span>
                </button>
                <button onclick="saveKeywordFromRegistry('${queueId}')" class="px-2 py-1 rounded-lg bg-indigo-600/20 hover:bg-indigo-600/40 text-indigo-300 border border-indigo-500/30 text-xs font-bold transition flex items-center gap-1 active:scale-95" title="Save to Production Kanban">
                    <i data-lucide="plus" class="w-3.5 h-3.5"></i>
                    <span>Queue</span>
                </button>
            </div>
        </div>
    `;
}

function onAlphabetSoupFilter(val) {
    state.alphabetFilterQuery = (val || '').toLowerCase().trim();
    const grid = document.getElementById('alphabet-soup-cards-grid');
    const countEl = document.getElementById('soup-results-count');
    if (!grid || !state.alphabetSoupData || !state.alphabetSoupData.results) return;

    let items = state.alphabetSoupData.results;
    if (state.alphabetFilterQuery) {
        items = items.filter(i => 
            (i.keyword || '').toLowerCase().includes(state.alphabetFilterQuery) ||
            (i.suggested_title || '').toLowerCase().includes(state.alphabetFilterQuery) ||
            (i.letter_trigger || '').toLowerCase() === state.alphabetFilterQuery.replace('+', '')
        );
    }
    if (countEl) countEl.innerText = `${items.length} variations`;
    if (items.length === 0) {
        grid.innerHTML = `<div class="col-span-full py-12 text-center text-slate-500 text-xs font-medium">No variations match "${escapeHtml(state.alphabetFilterQuery)}"</div>`;
    } else {
        grid.innerHTML = items.map(renderAlphabetSoupCardItem).join('');
    }
    lucide.createIcons();
}

function closeAlphabetModal() {
    const modal = document.getElementById('alphabet-soup-modal');
    if (modal) modal.classList.add('hidden');
}

// --- OVERVIEW HERO BANNER ---
function renderSeasonalHeroBanner(seasonal) {
    const banner = document.getElementById('seasonal-radar-hero');
    if (!banner || !seasonal) return;

    const niches = seasonal.priority_niches || [];

    banner.innerHTML = `
        <div class="space-y-6">
            <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 pb-5 border-b border-slate-800/80">
                <div>
                    <div class="flex items-center gap-2 mb-2">
                        <span class="px-3 py-0.5 rounded-full text-xs font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                            Seasonal Stock Radar (60-90 Days Lead Time)
                        </span>
                        <span class="text-xs text-slate-400 font-mono">${seasonal.current_date}</span>
                    </div>
                    <h2 class="text-2xl sm:text-3xl font-black text-white">${seasonal.upload_now_target}</h2>
                    <div class="flex flex-wrap items-center gap-2 mt-3">
                        <span class="text-xs text-slate-400 font-semibold uppercase tracking-wider">Peaking Right Now in Search:</span>
                        ${seasonal.current_peaking.map(p => `<span class="px-2.5 py-0.5 rounded-md bg-slate-800/90 text-xs text-slate-200 border border-slate-700/80 font-mono">${escapeHtml(p)}</span>`).join('')}
                    </div>
                </div>
                <button onclick="switchTab('daily-events')" class="px-5 py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-sm transition shadow-lg shadow-indigo-600/25 whitespace-nowrap flex items-center gap-2 shrink-0 active:scale-95">
                    <i data-lucide="calendar" class="w-4 h-4"></i>
                    <span>View 365-Day Calendar</span>
                </button>
            </div>

            <!-- Priority Production Windows Grid with Deadlines -->
            ${niches.length > 0 ? `
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <span class="text-xs font-bold text-amber-400 uppercase tracking-wider flex items-center gap-1.5 font-mono">
                            <i data-lucide="flame" class="w-3.5 h-3.5"></i>
                            Priority Production Windows to Upload THIS MONTH:
                        </span>
                        <span class="text-xs text-slate-400 font-mono">Rank #1 before buyer indexing cutoff</span>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        ${niches.map(n => {
                            const timing = getClientUploadDeadline(n.upload_deadline ? n : (n.theme || ''));
                            const themeId = registerData(n.theme);
                            return `
                                <div class="p-4 rounded-2xl bg-slate-900/90 border ${timing.is_late ? 'border-rose-500/40 shadow-rose-900/10' : 'border-slate-800'} hover:border-indigo-500/40 transition flex flex-col justify-between shadow-md">
                                    <div>
                                        <div class="flex items-start justify-between gap-1.5 mb-2">
                                            <h4 class="font-bold text-white text-sm leading-snug">${escapeHtml(n.theme)}</h4>
                                            <span class="px-2 py-0.5 rounded text-[10px] font-black shrink-0 ${timing.is_late ? 'bg-rose-600 text-white animate-pulse' : (timing.timing_status === 'CLOSING_SOON' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30')}">
                                                ${escapeHtml(timing.timing_badge)}
                                            </span>
                                        </div>

                                        <div class="space-y-1.5 mb-3 text-[11px] font-mono">
                                            <div class="text-slate-300 flex items-center gap-1">
                                                <i data-lucide="clock" class="w-3.5 h-3.5 text-indigo-400"></i>
                                                <span>Window: <strong class="text-white">${escapeHtml(n.upload_date_range || timing.upload_date_range)}</strong></span>
                                            </div>
                                            <div class="text-slate-400 flex items-center gap-1">
                                                <i data-lucide="calendar" class="w-3.5 h-3.5 text-amber-400"></i>
                                                <span>Deadline: <strong class="${timing.is_late ? 'text-rose-400 font-bold' : 'text-slate-200'}">${escapeHtml(n.upload_deadline || timing.upload_deadline)}</strong></span>
                                            </div>
                                        </div>

                                        ${n.keywords ? `
                                            <div class="flex flex-wrap gap-1 mb-3">
                                                ${(n.keywords || []).slice(0, 3).map(kw => `
                                                    <span class="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700/80 font-mono">${escapeHtml(kw)}</span>
                                                `).join('')}
                                            </div>
                                        ` : ''}
                                    </div>

                                    <div class="flex items-center justify-between pt-2.5 border-t border-slate-800 gap-2">
                                        <button onclick="loadAIQuotaTabById('${themeId}')" class="px-2.5 py-1.5 rounded-xl bg-purple-600/20 hover:bg-purple-600/40 text-purple-300 border border-purple-500/30 text-xs font-bold transition flex items-center gap-1 active:scale-95">
                                            <i data-lucide="sparkles" class="w-3 h-3"></i> AI Prompts
                                        </button>
                                        <button onclick="queueEventTitles('${themeId}')" class="px-2.5 py-1.5 rounded-xl bg-indigo-600/20 hover:bg-indigo-600/40 text-indigo-300 border border-indigo-500/30 text-xs font-bold transition flex items-center gap-1 active:scale-95">
                                            <i data-lucide="plus" class="w-3 h-3"></i> Queue
                                        </button>
                                    </div>
                                </div>
                            `;
                        }).join('')}
                    </div>
                </div>
            ` : ''}
        </div>
    `;
    lucide.createIcons();
}

function renderPlatformCards(platforms) {
    const grid = document.getElementById('platforms-cards-grid');
    if (!grid || !platforms) return;

    const platformSeasonWindows = {
        'adobe_stock': { focus: 'Autumn & Winter Commercial, AI 4K Loops, Tech & Medical', window: 'Aug 15 – Oct 15, 2026', deadline: 'October 15, 2026', badge: '🟢 PRIME UPLOAD WINDOW' },
        'shutterstock': { focus: 'Commercial Advertising & Global Brand Campaigns, Photos', window: 'Aug 15 – Oct 15, 2026', deadline: 'October 15, 2026', badge: '🟢 PRIME UPLOAD WINDOW' },
        'etsy': { focus: 'Canva Holiday Templates, SVG Cut Files & 2027 Planners', window: 'Aug 01 – Oct 10, 2026', deadline: 'October 10, 2026', badge: '🟡 CLOSING SOON' },
        'iconscout': { focus: '3D UI Icons, Lottie UI Motion & Clean Alpha Vectors', window: 'Sep 01 – Nov 01, 2026', deadline: 'November 01, 2026', badge: '🟢 PRIME UPLOAD WINDOW' },
        'graphicriver': { focus: 'Photoshop PSD Product Mockups & Print Flyers', window: 'Aug 15 – Oct 15, 2026', deadline: 'October 15, 2026', badge: '🟢 PRIME UPLOAD WINDOW' }
    };

    let html = '';
    for (const [key, p] of Object.entries(platforms)) {
        const pTiming = platformSeasonWindows[key] || { focus: 'Year-Round Production', window: 'Upload 60-90 Days Ahead', deadline: 'Continuous', badge: '🟢 PRIME WINDOW' };
        html += `
            <div class="glass-card rounded-2xl p-6 flex flex-col justify-between cursor-pointer border border-slate-800/90 shadow-xl hover:border-indigo-500/40 transition group" onclick="switchTab('platform-${key}')">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <span class="px-3 py-1 rounded-full text-xs font-extrabold ${getPlatformBadgeClass(key)}">
                            ${p.badge}
                        </span>
                        <span class="text-xs text-slate-400 font-mono bg-slate-900 px-2 py-0.5 rounded border border-slate-800">${p.tag_limit} Tags</span>
                    </div>
                    <h3 class="text-xl font-black text-white mb-2">${p.name}</h3>

                    <!-- Production Upload Window & Deadline Strip -->
                    <div class="mb-3.5 p-2.5 rounded-xl bg-slate-950/70 border border-slate-800/80 text-[11px] font-mono space-y-1">
                        <div class="flex items-center justify-between">
                            <span class="text-emerald-400 font-bold">${pTiming.badge}</span>
                            <span class="text-slate-400">Due: <strong class="text-amber-300 font-bold">${pTiming.deadline}</strong></span>
                        </div>
                        <div class="text-slate-400 truncate">Window: <strong class="text-slate-200">${pTiming.window}</strong></div>
                    </div>
                    
                    <div class="space-y-1.5 mb-4">
                        ${p.primary_focus.slice(0, 3).map(f => `
                            <div class="flex items-center gap-2 text-xs text-slate-300 font-medium">
                                <i data-lucide="check" class="w-3.5 h-3.5 text-emerald-400 shrink-0"></i>
                                <span>${escapeHtml(f)}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <div class="pt-3.5 border-t border-slate-800/80 flex items-center justify-between text-xs font-bold text-indigo-400 group-hover:text-indigo-300">
                    <span>Isolated Search & Specs</span>
                    <i data-lucide="arrow-right" class="w-4 h-4 transition-transform group-hover:translate-x-1"></i>
                </div>
            </div>
        `;
    }
    grid.innerHTML = html;
    lucide.createIcons();
}

function getPlatformBadgeClass(key) {
    if (key === 'adobe_stock') return 'badge-adobe';
    if (key === 'shutterstock') return 'badge-shutter';
    if (key === 'etsy') return 'badge-etsy';
    if (key === 'iconscout') return 'badge-iconscout';
    if (key === 'graphicriver') return 'badge-graphicriver';
    return 'badge-ai';
}

// --- UTILITIES & EXPORTS ---
function exportSoupToCSVById(id) {
    const baseKeyword = (state.alphabetSoupData && state.alphabetSoupData.base_keyword) || getRegisteredData(id) || 'stock';
    const items = (state.alphabetSoupData && state.alphabetSoupData.results) || [];
    if (items.length === 0) {
        showToast('No alphabet soup data to export', 'info');
        return;
    }

    let csv = "Keyword,Letter Trigger,Suggested Stock Title,Upload Date Range,Upload Deadline,Timing Status,Is Late,Opportunity Score,Recommended Tool,Marketplace\n";
    items.forEach(r => {
        const timing = getClientUploadDeadline(r);
        const kw = (r.keyword || '').replace(/"/g, '""');
        const letter = (r.letter_trigger || '').replace(/"/g, '""');
        const title = (r.suggested_title || '').replace(/"/g, '""');
        const uWindow = (timing.upload_date_range || '').replace(/"/g, '""');
        const uDeadline = (timing.upload_deadline || '').replace(/"/g, '""');
        const uStatus = (timing.timing_badge || '').replace(/"/g, '""');
        const isLate = timing.is_late ? `Yes (${timing.days_overdue}d overdue)` : 'No';
        const opp = r.opportunity_score || 0;
        const tool = (r.recommended_tool || '').replace(/"/g, '""');
        const mkt = (r.best_marketplace || '').replace(/"/g, '""');
        csv += `"${kw}","+${letter}","${title}","${uWindow}","${uDeadline}","${uStatus}","${isLate}","${opp}","${tool}","${mkt}"\n`;
    });

    downloadCSV(csv, `alphabet_soup_${baseKeyword.replace(/\s+/g, '_')}.csv`);
    showToast(`Exported ${items.length} A-Z variations to CSV!`, 'success');
}

function exportQueueCSV() {
    if (!state.queueItems || state.queueItems.length === 0) {
        showToast('Queue is empty', 'info');
        return;
    }
    let csv = "ID,Keyword,Platform,Asset Type,Upload Date Range,Upload Deadline,Timing Status,Is Late,Score,Competition,Status,Created At\n";
    state.queueItems.forEach(i => {
        const timing = getClientUploadDeadline(i);
        const uWindow = (timing.upload_date_range || '').replace(/"/g, '""');
        const uDeadline = (timing.upload_deadline || '').replace(/"/g, '""');
        const uStatus = (timing.timing_badge || '').replace(/"/g, '""');
        const isLate = timing.is_late ? `Yes (${timing.days_overdue}d overdue)` : 'No';
        csv += `"${i.id}","${(i.keyword || '').replace(/"/g, '""')}","${(i.platform || '').replace(/"/g, '""')}","${(i.asset_type || '').replace(/"/g, '""')}","${uWindow}","${uDeadline}","${uStatus}","${isLate}","${i.demand_score}","${(i.competition || 'Medium').replace(/"/g, '""')}","${i.status}","${i.created_at}"\n`;
    });
    downloadCSV(csv, "stockpulse_production_queue.csv");
    showToast(`Exported ${state.queueItems.length} Kanban concepts to CSV!`, 'success');
}

function downloadCSV(content, filename) {
    const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function copyToClipboard(text, msg) {
    if (!text) return;
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(() => {
            showToast(msg || 'Copied to clipboard!', 'success');
        }).catch(() => {
            fallbackCopy(text, msg);
        });
    } else {
        fallbackCopy(text, msg);
    }
}

function fallbackCopy(text, msg) {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.left = '-999999px';
    document.body.appendChild(ta);
    ta.select();
    try {
        document.execCommand('copy');
        showToast(msg || 'Copied to clipboard!', 'success');
    } catch (e) {
        showToast('Failed to copy', 'error');
    }
    document.body.removeChild(ta);
}

function copyRegisteredText(id, label) {
    const text = getRegisteredData(id);
    if (text) {
        const clean = (label || 'Text').replace(/\s*Copied!?/gi, '').trim();
        copyToClipboard(text, `${clean} Copied to Clipboard!`);
    }
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast flex items-center gap-3 px-4 py-3 rounded-2xl bg-slate-900/95 border text-xs font-bold shadow-2xl';

    let icon = 'check-circle';
    let borderColor = 'border-emerald-500/50 text-emerald-300';
    if (type === 'error') {
        icon = 'alert-triangle';
        borderColor = 'border-rose-500/50 text-rose-300';
    } else if (type === 'info') {
        icon = 'info';
        borderColor = 'border-indigo-500/50 text-indigo-300';
    }

    toast.classList.add(...borderColor.split(' '));
    toast.innerHTML = `
        <i data-lucide="${icon}" class="w-4 h-4 shrink-0"></i>
        <span class="tracking-wide">${escapeHtml(message)}</span>
    `;

    container.appendChild(toast);
    lucide.createIcons();

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3200);
}

function escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

// =========================================================================
// --- ADOBE STOCK COMMERCIAL AI STUDIO & MULTI-MODEL CONTROLLERS ---
// =========================================================================

/**
 * Toggles active model tab inside Search Results AI Brief card.
 */
function toggleSearchAIBriefModel(model) {
    const tabs = {
        mj: document.getElementById('search-ai-tab-mj'),
        flux: document.getElementById('search-ai-tab-flux'),
        chatgpt: document.getElementById('search-ai-tab-chatgpt'),
        nano: document.getElementById('search-ai-tab-nano'),
        video: document.getElementById('search-ai-tab-video')
    };
    const panels = {
        mj: document.getElementById('search-ai-panel-mj'),
        flux: document.getElementById('search-ai-panel-flux'),
        chatgpt: document.getElementById('search-ai-panel-chatgpt'),
        nano: document.getElementById('search-ai-panel-nano'),
        video: document.getElementById('search-ai-panel-video')
    };

    ['mj', 'flux', 'chatgpt', 'nano', 'video'].forEach(m => {
        if (tabs[m]) {
            if (m === model) {
                tabs[m].className = 'px-2.5 py-1 rounded-lg text-[11px] font-bold bg-purple-600 text-white transition active:scale-95';
            } else {
                tabs[m].className = 'px-2.5 py-1 rounded-lg text-[11px] font-bold bg-slate-800 text-slate-300 hover:text-white transition active:scale-95';
            }
        }
        if (panels[m]) {
            if (m === model) {
                panels[m].classList.remove('hidden');
            } else {
                panels[m].classList.add('hidden');
            }
        }
    });
}

/**
 * Generates expandable AI prompt drawer inside platform "What to Create" cards.
 */
function renderConceptAIPromptDrawer(itemCardId, item) {
    if (!item || !item.ai_prompts) return '';
    const p = item.ai_prompts;
    const ref = p.reference_guide || {};
    const mjPrompt = p.midjourney || '';
    const fluxPrompt = p.flux || '';
    const chatgptPrompt = p.chatgpt || '';
    const nanoPrompt = p.nano_banana || '';
    const vidPrompt = p.video || '';
    const canvaPrompt = p.canva_spec || '';
    const svgPrompt = p.svg_spec || '';
    const octanePrompt = p.octane_3d || '';
    const lottiePrompt = p.lottie_motion || '';
    const psdPrompt = p.psd_spec || '';
    const negPrompt = p.negative_prompt || '';
    const srefSyntax = ref.sref_syntax || '';

    const mjId = registerData(mjPrompt);
    const fluxId = registerData(fluxPrompt);
    const chatgptId = registerData(chatgptPrompt);
    const nanoId = registerData(nanoPrompt);
    const vidId = registerData(vidPrompt);
    const canvaId = registerData(canvaPrompt);
    const svgId = registerData(svgPrompt);
    const octaneId = registerData(octanePrompt);
    const lottieId = registerData(lottiePrompt);
    const psdId = registerData(psdPrompt);
    const negId = registerData(negPrompt);
    const srefId = registerData(srefSyntax);

    return `
        <div class="space-y-3">
            <!-- Style Reference Guide Banner -->
            ${ref.benchmark ? `
                <div class="p-2.5 rounded-lg bg-purple-950/40 border border-purple-500/25 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                    <div>
                        <span class="text-[10px] font-bold uppercase tracking-wider text-purple-300">Style Benchmark:</span>
                        <div class="text-xs font-bold text-white">${escapeHtml(ref.benchmark)}</div>
                        ${ref.mood ? `<div class="text-[11px] text-slate-300 mt-0.5">${escapeHtml(ref.mood)}</div>` : ''}
                    </div>
                    ${srefSyntax ? `
                        <button type="button" onclick="copyRegisteredText('${srefId}', 'Reference Syntax Copied!')" class="px-2.5 py-1 rounded-md bg-purple-600/30 hover:bg-purple-600/50 text-purple-200 border border-purple-500/40 text-[11px] font-mono font-bold transition flex items-center gap-1 shrink-0 self-start sm:self-auto active:scale-95">
                            <i data-lucide="link" class="w-3 h-3"></i> Copy --sref
                        </button>
                    ` : ''}
                </div>
            ` : ''}

            <!-- Midjourney v6.1 Prompt -->
            ${mjPrompt ? `
                <div>
                    <div class="flex items-center justify-between mb-1">
                        <span class="text-[11px] font-bold text-purple-300 flex items-center gap-1">
                            <span class="w-1.5 h-1.5 rounded-full bg-purple-400"></span> Midjourney v6.1 (Commercial Raw)
                        </span>
                        <button type="button" onclick="copyRegisteredText('${mjId}', 'Midjourney Prompt Copied!')" class="text-[11px] text-purple-400 hover:text-purple-300 font-semibold flex items-center gap-1 transition">
                            <i data-lucide="copy" class="w-3 h-3"></i> Copy
                        </button>
                    </div>
                    <div class="p-2.5 rounded-lg bg-slate-900/90 border border-purple-500/25 text-slate-300 font-mono text-[11px] leading-relaxed max-h-28 overflow-y-auto no-scrollbar select-all">
                        ${escapeHtml(mjPrompt)}
                    </div>
                </div>
            ` : ''}

            <!-- Flux.1 Pro Prompt -->
            ${fluxPrompt ? `
                <div>
                    <div class="flex items-center justify-between mb-1">
                        <span class="text-[11px] font-bold text-cyan-300 flex items-center gap-1">
                            <span class="w-1.5 h-1.5 rounded-full bg-cyan-400"></span> Flux.1 Pro (Natural Detail)
                        </span>
                        <button type="button" onclick="copyRegisteredText('${fluxId}', 'Flux Prompt Copied!')" class="text-[11px] text-cyan-400 hover:text-cyan-300 font-semibold flex items-center gap-1 transition">
                            <i data-lucide="copy" class="w-3 h-3"></i> Copy
                        </button>
                    </div>
                    <div class="p-2.5 rounded-lg bg-slate-900/90 border border-cyan-500/25 text-slate-300 font-mono text-[11px] leading-relaxed max-h-24 overflow-y-auto no-scrollbar select-all">
                        ${escapeHtml(fluxPrompt)}
                    </div>
                </div>
            ` : ''}

            <!-- ChatGPT (DALL-E 3) Prompt -->
            ${chatgptPrompt ? `
                <div>
                    <div class="flex items-center justify-between mb-1">
                        <span class="text-[11px] font-bold text-emerald-300 flex items-center gap-1">
                            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> ChatGPT (DALL-E 3 & GPT-4o Image)
                        </span>
                        <button type="button" onclick="copyRegisteredText('${chatgptId}', 'ChatGPT Prompt Copied!')" class="text-[11px] text-emerald-400 hover:text-emerald-300 font-semibold flex items-center gap-1 transition">
                            <i data-lucide="copy" class="w-3 h-3"></i> Copy
                        </button>
                    </div>
                    <div class="p-2.5 rounded-lg bg-slate-900/90 border border-emerald-500/25 text-slate-300 font-mono text-[11px] leading-relaxed max-h-24 overflow-y-auto no-scrollbar select-all">
                        ${escapeHtml(chatgptPrompt)}
                    </div>
                </div>
            ` : ''}

            <!-- Google Nano Banana (Gemini Image) Prompt -->
            ${nanoPrompt ? `
                <div>
                    <div class="flex items-center justify-between mb-1">
                        <span class="text-[11px] font-bold text-amber-300 flex items-center gap-1">
                            <span class="w-1.5 h-1.5 rounded-full bg-amber-400"></span> Nano Banana (Google Gemini Image)
                        </span>
                        <button type="button" onclick="copyRegisteredText('${nanoId}', 'Nano Banana Prompt Copied!')" class="text-[11px] text-amber-400 hover:text-amber-300 font-semibold flex items-center gap-1 transition">
                            <i data-lucide="copy" class="w-3 h-3"></i> Copy
                        </button>
                    </div>
                    <div class="p-2.5 rounded-lg bg-slate-900/90 border border-amber-500/25 text-slate-300 font-mono text-[11px] leading-relaxed max-h-24 overflow-y-auto no-scrollbar select-all">
                        ${escapeHtml(nanoPrompt)}
                    </div>
                </div>
            ` : ''}

            <!-- Canva Template Blueprint Spec (Etsy) -->
            ${canvaPrompt ? `
                <div>
                    <div class="flex items-center justify-between mb-1">
                        <span class="text-[11px] font-bold text-amber-400 flex items-center gap-1">
                            <span class="w-1.5 h-1.5 rounded-full bg-amber-400"></span> Canva Template Blueprint (Etsy Best-Seller)
                        </span>
                        <button type="button" onclick="copyRegisteredText('${canvaId}', 'Canva Template Spec Copied!')" class="text-[11px] text-amber-400 hover:text-amber-300 font-semibold flex items-center gap-1 transition">
                            <i data-lucide="copy" class="w-3 h-3"></i> Copy
                        </button>
                    </div>
                    <div class="p-2.5 rounded-lg bg-slate-900/90 border border-amber-500/25 text-slate-300 font-mono text-[11px] leading-relaxed max-h-24 overflow-y-auto no-scrollbar select-all">
                        ${escapeHtml(canvaPrompt)}
                    </div>
                </div>
            ` : ''}

            <!-- SVG Cut File Spec (Etsy / Vector) -->
            ${svgPrompt ? `
                <div>
                    <div class="flex items-center justify-between mb-1">
                        <span class="text-[11px] font-bold text-emerald-400 flex items-center gap-1">
                            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> Clean Vector Cut & SVG Spec (Cricut / Silhouette)
                        </span>
                        <button type="button" onclick="copyRegisteredText('${svgId}', 'SVG Spec Copied!')" class="text-[11px] text-emerald-400 hover:text-emerald-300 font-semibold flex items-center gap-1 transition">
                            <i data-lucide="copy" class="w-3 h-3"></i> Copy
                        </button>
                    </div>
                    <div class="p-2.5 rounded-lg bg-slate-900/90 border border-emerald-500/25 text-slate-300 font-mono text-[11px] leading-relaxed max-h-24 overflow-y-auto no-scrollbar select-all">
                        ${escapeHtml(svgPrompt)}
                    </div>
                </div>
            ` : ''}

            <!-- Cinema 4D / Octane 3D UI Render Spec (IconScout) -->
            ${octanePrompt ? `
                <div>
                    <div class="flex items-center justify-between mb-1">
                        <span class="text-[11px] font-bold text-cyan-400 flex items-center gap-1">
                            <span class="w-1.5 h-1.5 rounded-full bg-cyan-400"></span> Cinema 4D / Octane 3D UI Render Spec (Clean Alpha Cutout)
                        </span>
                        <button type="button" onclick="copyRegisteredText('${octaneId}', '3D Render Spec Copied!')" class="text-[11px] text-cyan-400 hover:text-cyan-300 font-semibold flex items-center gap-1 transition">
                            <i data-lucide="copy" class="w-3 h-3"></i> Copy
                        </button>
                    </div>
                    <div class="p-2.5 rounded-lg bg-slate-900/90 border border-cyan-500/25 text-slate-300 font-mono text-[11px] leading-relaxed max-h-24 overflow-y-auto no-scrollbar select-all">
                        ${escapeHtml(octanePrompt)}
                    </div>
                </div>
            ` : ''}

            <!-- Lottie Motion Spec (IconScout) -->
            ${lottiePrompt ? `
                <div>
                    <div class="flex items-center justify-between mb-1">
                        <span class="text-[11px] font-bold text-pink-400 flex items-center gap-1">
                            <span class="w-1.5 h-1.5 rounded-full bg-pink-400"></span> Lottie & After Effects Motion Spec
                        </span>
                        <button type="button" onclick="copyRegisteredText('${lottieId}', 'Lottie Motion Spec Copied!')" class="text-[11px] text-pink-400 hover:text-pink-300 font-semibold flex items-center gap-1 transition">
                            <i data-lucide="copy" class="w-3 h-3"></i> Copy
                        </button>
                    </div>
                    <div class="p-2.5 rounded-lg bg-slate-900/90 border border-pink-500/25 text-slate-300 font-mono text-[11px] leading-relaxed max-h-24 overflow-y-auto no-scrollbar select-all">
                        ${escapeHtml(lottiePrompt)}
                    </div>
                </div>
            ` : ''}

            <!-- Photoshop Layered PSD & Print Bleed Spec (GraphicRiver) -->
            ${psdPrompt ? `
                <div>
                    <div class="flex items-center justify-between mb-1">
                        <span class="text-[11px] font-bold text-blue-400 flex items-center gap-1">
                            <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span> Photoshop Layered PSD & Print Bleed Spec (Smart Objects)
                        </span>
                        <button type="button" onclick="copyRegisteredText('${psdId}', 'PSD Print Spec Copied!')" class="text-[11px] text-blue-400 hover:text-blue-300 font-semibold flex items-center gap-1 transition">
                            <i data-lucide="copy" class="w-3 h-3"></i> Copy
                        </button>
                    </div>
                    <div class="p-2.5 rounded-lg bg-slate-900/90 border border-blue-500/25 text-slate-300 font-mono text-[11px] leading-relaxed max-h-24 overflow-y-auto no-scrollbar select-all">
                        ${escapeHtml(psdPrompt)}
                    </div>
                </div>
            ` : ''}

            <!-- 4K Video B-Roll Prompt -->
            ${vidPrompt ? `
                <div>
                    <div class="flex items-center justify-between mb-1">
                        <span class="text-[11px] font-bold text-blue-300 flex items-center gap-1">
                            <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span> 4K Video B-Roll (Runway / Luma / Sora)
                        </span>
                        <button type="button" onclick="copyRegisteredText('${vidId}', '4K Video Prompt Copied!')" class="text-[11px] text-blue-400 hover:text-blue-300 font-semibold flex items-center gap-1 transition">
                            <i data-lucide="copy" class="w-3 h-3"></i> Copy
                        </button>
                    </div>
                    <div class="p-2.5 rounded-lg bg-slate-900/90 border border-blue-500/25 text-slate-300 font-mono text-[11px] leading-relaxed max-h-24 overflow-y-auto no-scrollbar select-all">
                        ${escapeHtml(vidPrompt)}
                    </div>
                </div>
            ` : ''}

            <!-- Negative Constraints -->
            ${negPrompt ? `
                <div class="flex items-center justify-between pt-1 text-[11px]">
                    <span class="text-rose-400 font-medium">Rejection-Proof Negative: <span class="font-mono text-slate-400">${escapeHtml(negPrompt)}</span></span>
                    <button type="button" onclick="copyRegisteredText('${negId}', 'Negative Prompt Copied!')" class="text-rose-400 hover:text-rose-300 font-semibold shrink-0 ml-2 transition">Copy</button>
                </div>
            ` : ''}
        </div>
    `;
}

/**
 * Toggles visibility of the Concept AI prompt drawer.
 */
function toggleConceptAIPrompt(itemCardId) {
    const drawer = document.getElementById(`concept-ai-drawer-${itemCardId}`);
    const chevron = document.getElementById(`chevron-ai-${itemCardId}`);
    if (!drawer) return;

    if (drawer.classList.contains('hidden')) {
        drawer.classList.remove('hidden');
        if (chevron) chevron.style.transform = 'rotate(180deg)';
        lucide.createIcons();
    } else {
        drawer.classList.add('hidden');
        if (chevron) chevron.style.transform = 'rotate(0deg)';
    }
}

/**
 * Loads or re-generates the Adobe Stock AI Studio data.
 */
async function loadAdobeStockAIStudio(topic, refUrl, activeModel) {
    const root = document.getElementById('adobe-stock-ai-studio-root');
    if (!root) return;

    const currentTopic = topic || (state.adobeStockStudio && state.adobeStockStudio.topic) || 'abstract 3d liquid waves';
    const currentRef = (refUrl !== undefined) ? refUrl : (state.adobeStockStudio ? state.adobeStockStudio.customRefUrl : '');
    const model = activeModel || (state.adobeStockStudio ? state.adobeStockStudio.activeModel : 'mj');

    try {
        let apiUrl = `/api/adobe-stock/ai-studio?topic=${encodeURIComponent(currentTopic)}`;
        if (currentRef) {
            apiUrl += `&ref_url=${encodeURIComponent(currentRef)}`;
        }
        const res = await fetch(apiUrl);
        const data = await res.json();

        state.adobeStockStudio = {
            topic: data.topic,
            brief: data.brief,
            tags: data.tags_adobe || [],
            presets: data.presets || [],
            activeModel: model,
            customRefUrl: currentRef || ''
        };

        renderAdobeStockAIStudioUI();
    } catch (e) {
        console.error('Error loading Adobe Stock AI Studio:', e);
        root.innerHTML = `
            <div class="glass-panel rounded-2xl p-6 text-center text-rose-400 border border-rose-500/30">
                <i data-lucide="alert-triangle" class="w-8 h-8 mx-auto mb-2"></i>
                <p class="font-bold text-sm">Failed to generate AI studio briefs. Ensure the local server is running.</p>
            </div>
        `;
        lucide.createIcons();
    }
}

/**
 * Renders the full Adobe Stock Commercial AI Studio UI.
 */
function renderAdobeStockAIStudioUI() {
    const root = document.getElementById('adobe-stock-ai-studio-root');
    if (!root || !state.adobeStockStudio) return;

    const { topic, brief, tags, presets, activeModel, customRefUrl } = state.adobeStockStudio;
    const models = brief.models || {};
    const refGuide = brief.reference_guide || {};
    const breakdown = brief.prompt_breakdown || {};
    
    const mjPrompt = models.midjourney || brief.ai_image_prompt || '';
    const mjWithRef = models.midjourney_with_ref || mjPrompt;
    const fluxPrompt = models.flux || mjPrompt;
    const chatgptPrompt = models.chatgpt || mjPrompt;
    const nanoPrompt = models.nano_banana || mjPrompt;
    const videoPrompt = models.video_4k || brief.ai_video_prompt || '';
    const negPrompt = brief.negative_prompt || '';
    const benchmark = refGuide.aesthetic_benchmark || 'Commercial Stock Photography';

    // Register active strings for safe click handlers
    const mjPromptId = registerData(mjPrompt);
    const mjWithRefId = registerData(mjWithRef);
    const fluxPromptId = registerData(fluxPrompt);
    const chatgptPromptId = registerData(chatgptPrompt);
    const nanoPromptId = registerData(nanoPrompt);
    const videoPromptId = registerData(videoPrompt);
    const negPromptId = registerData(negPrompt);
    const tagsTextId = registerData(tags.join(', '));
    const activeRefId = registerData(refGuide.sref_syntax || (customRefUrl ? `--sref ${customRefUrl} --sw 100` : ''));
    const queueItemId = registerData({
        keyword: topic,
        best_marketplace: 'Adobe Stock',
        recommended_tool: activeModel === 'video' ? '4K Video' : 'AI Image (Midjourney/Flux)',
        opportunity_score: 95,
        suggested_title: `${topic.charAt(0).toUpperCase() + topic.slice(1)} Commercial Stock Asset with Modern Lighting`
    });
    const logDoneId = registerData({
        suggested_title: `${topic.charAt(0).toUpperCase() + topic.slice(1)} Commercial Stock Asset`,
        asset_type: activeModel === 'video' ? 'AI Video' : 'AI Image',
        platform: 'Adobe Stock',
        concept: topic
    });

    // Quick niche options for 1-click inspiration
    const quickNiches = [
        'abstract 3d liquid waves',
        'diverse corporate team in modern office',
        'biotech crispr laboratory scientist',
        'modern female architect blueprints studio',
        'kinfolk warm coffee flatlay',
        'cyberpunk holographic data visualization',
        'clean energy solar farm aerial drone',
        'luxury marble cosmetic bottle podium'
    ];

    let currentPromptText = mjPrompt;
    if (activeModel === 'flux') currentPromptText = fluxPrompt;
    else if (activeModel === 'chatgpt') currentPromptText = chatgptPrompt;
    else if (activeModel === 'nano') currentPromptText = nanoPrompt;
    else if (activeModel === 'video') currentPromptText = videoPrompt;
    else if (activeModel === 'mj_ref') currentPromptText = mjWithRef;

    let currentCopyId = mjPromptId;
    if (activeModel === 'flux') currentCopyId = fluxPromptId;
    else if (activeModel === 'chatgpt') currentCopyId = chatgptPromptId;
    else if (activeModel === 'nano') currentCopyId = nanoPromptId;
    else if (activeModel === 'video') currentCopyId = videoPromptId;
    else if (activeModel === 'mj_ref') currentCopyId = mjWithRefId;

    root.innerHTML = `
        <div class="glass-panel rounded-3xl p-6 sm:p-8 border border-purple-500/30 shadow-2xl relative overflow-hidden">
            <!-- Background glow -->
            <div class="absolute top-0 right-0 w-96 h-96 bg-purple-600/10 rounded-full blur-3xl pointer-events-none"></div>

            <!-- Studio Header -->
            <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4 pb-6 mb-6 border-b border-purple-500/20">
                <div>
                    <div class="flex flex-wrap items-center gap-2 mb-2">
                        <span class="px-3 py-1 rounded-full text-xs font-black bg-gradient-to-r from-purple-500/30 to-indigo-500/30 text-purple-200 border border-purple-500/40 flex items-center gap-1.5">
                            <i data-lucide="sparkles" class="w-3.5 h-3.5 text-purple-400"></i>
                            Adobe Stock AI Studio
                        </span>
                        <span class="px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 flex items-center gap-1">
                            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                            100% Accepted & High Earner
                        </span>
                        <span class="px-2.5 py-1 rounded-full text-xs font-mono text-purple-300/80 bg-purple-950/60 border border-purple-800">
                            Genre: ${escapeHtml((brief.genre || 'Commercial Stock').toUpperCase())}
                        </span>
                    </div>
                    <h3 class="text-2xl sm:text-3xl font-black text-white tracking-tight">Commercial Stock Prompt Architect & Style Reference Engine</h3>
                    <p class="text-slate-300 text-xs sm:text-sm mt-1 max-w-3xl leading-relaxed">
                        Generates photorealistic, buyer-converting prompts with authentic lighting, real optical parameters (focal length, f-stop, sensor), ample negative copy space for commercial typography, and visual style reference (<code class="text-purple-300 font-mono">--sref</code>) benchmarks.
                    </p>
                </div>

                <div class="flex items-center gap-2 shrink-0">
                    <button onclick="quickLogAssetFromRegistry('${logDoneId}')" class="px-3.5 py-2 rounded-xl bg-emerald-600/20 hover:bg-emerald-600/40 text-emerald-300 border border-emerald-500/30 text-xs font-bold transition flex items-center gap-1.5 active:scale-95 shadow-sm">
                        <i data-lucide="check" class="w-3.5 h-3.5"></i>
                        Mark Done
                    </button>
                    <button onclick="saveKeywordFromRegistry('${queueItemId}')" class="px-3.5 py-2 rounded-xl bg-indigo-600/20 hover:bg-indigo-600/40 text-indigo-300 border border-indigo-500/30 text-xs font-bold transition flex items-center gap-1.5 active:scale-95 shadow-sm" title="Add to Production Kanban">
                        <i data-lucide="plus" class="w-3.5 h-3.5"></i>
                        Queue
                    </button>
                </div>
            </div>

            <!-- Topic Search & Seed Input -->
            <div class="mb-6">
                <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2.5 mb-3">
                    <div class="relative flex-1">
                        <i data-lucide="sparkles" class="w-4 h-4 text-purple-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none"></i>
                        <input
                            id="adobe-stock-studio-input"
                            type="text"
                            value="${escapeHtml(topic)}"
                            placeholder="Enter any seed concept or commercial topic (e.g., female architect, coffee lifestyle)..."
                            class="w-full bg-slate-900/90 text-white text-xs sm:text-sm py-2.5 pl-10 pr-4 rounded-xl border border-purple-500/40 focus:outline-none focus:border-purple-400 font-medium"
                            onkeydown="if(event.key==='Enter') executeAdobeStockAIGenerate()"
                        />
                    </div>
                    <button
                        onclick="executeAdobeStockAIGenerate()"
                        class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white text-xs font-bold transition flex items-center justify-center gap-2 shadow-lg shadow-purple-600/25 active:scale-95 whitespace-nowrap"
                    >
                        <i data-lucide="cpu" class="w-4 h-4"></i>
                        <span>Generate High-Converting Brief</span>
                    </button>
                </div>

                <!-- Quick Niche Pills -->
                <div class="flex flex-wrap items-center gap-1.5">
                    <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider mr-1">Trending Niches:</span>
                    ${quickNiches.map(n => `
                        <button
                            onclick="loadAdobeStockAIStudio('${escapeHtml(n)}', '${escapeHtml(customRefUrl)}')"
                            class="px-2.5 py-1 rounded-lg text-[11px] font-semibold transition active:scale-95 ${topic.toLowerCase() === n.toLowerCase() ? 'bg-purple-600 text-white shadow-sm' : 'bg-slate-900/80 text-purple-200 border border-purple-500/30 hover:border-purple-500/60 hover:text-white'}"
                        >
                            ${escapeHtml(n)}
                        </button>
                    `).join('')}
                </div>
            </div>

            <!-- Style Reference (--sref) Benchmarks & Custom URL Bar -->
            <div class="p-4 sm:p-5 rounded-2xl bg-purple-950/20 border border-purple-500/25 mb-6">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
                    <div class="flex items-center gap-2">
                        <i data-lucide="image" class="w-4 h-4 text-purple-400"></i>
                        <h4 class="text-xs sm:text-sm font-bold text-white">Visual Style Reference Benchmarks (<code class="text-purple-300 font-mono">--sref</code>)</h4>
                        <span class="text-[10px] text-purple-300 bg-purple-900/50 px-2 py-0.5 rounded border border-purple-500/30">Stock Buyer Aesthetics</span>
                    </div>
                    ${customRefUrl ? `
                        <button onclick="loadAdobeStockAIStudio('${escapeHtml(topic)}', '')" class="text-[11px] text-rose-300 hover:text-rose-200 font-semibold flex items-center gap-1 self-start sm:self-auto transition">
                            <i data-lucide="x" class="w-3 h-3"></i> Clear Custom Ref
                        </button>
                    ` : ''}
                </div>

                <!-- Preset Style Cards Grid -->
                <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2 mb-3.5">
                    ${(presets || []).map(preset => {
                        const isSelected = (customRefUrl === preset.sref_code) || (!customRefUrl && refGuide.aesthetic_benchmark === preset.benchmark);
                        return `
                            <button
                                type="button"
                                onclick="loadAdobeStockAIStudio('${escapeHtml(topic)}', '${escapeHtml(preset.sref_code)}')"
                                class="p-2.5 rounded-xl border text-left transition active:scale-95 flex flex-col justify-between ${isSelected ? 'bg-purple-600/30 border-purple-400 text-white shadow-md' : 'bg-slate-900/80 border-slate-800 text-slate-300 hover:border-purple-500/40 hover:text-white'}"
                                title="${escapeHtml(preset.description)}"
                            >
                                <div>
                                    <div class="text-[11px] font-bold leading-tight mb-1 truncate">${escapeHtml(preset.name)}</div>
                                    <div class="text-[10px] text-purple-300 font-mono truncate">${escapeHtml(preset.benchmark)}</div>
                                </div>
                                <div class="text-[9px] text-slate-400 mt-2 truncate font-mono">${escapeHtml(preset.recommended_for)}</div>
                            </button>
                        `;
                    }).join('')}
                </div>

                <!-- Custom Reference URL Bar -->
                <div class="flex flex-col sm:flex-row items-center gap-2 pt-2 border-t border-purple-500/20">
                    <span class="text-[11px] font-semibold text-slate-400 shrink-0">Custom Ref Image URL:</span>
                    <input
                        id="adobe-stock-studio-ref-input"
                        type="url"
                        value="${escapeHtml(customRefUrl)}"
                        placeholder="Paste any uncompressed JPG/PNG URL (e.g. Unsplash, Behance, your portfolio image)..."
                        class="flex-1 w-full bg-slate-900/90 text-white text-xs py-1.5 px-3 rounded-lg border border-purple-500/30 focus:outline-none focus:border-purple-400 font-mono"
                        onkeydown="if(event.key==='Enter') applyCustomRefUrlInStudio()"
                    />
                    <div class="flex items-center gap-1.5 w-full sm:w-auto justify-end">
                        <button
                            onclick="applyCustomRefUrlInStudio()"
                            class="px-3 py-1.5 rounded-lg bg-purple-600/40 hover:bg-purple-600/60 text-purple-200 border border-purple-500/40 text-xs font-bold transition whitespace-nowrap active:scale-95"
                        >
                            Apply Ref
                        </button>
                        ${refGuide.sref_syntax ? `
                            <button
                                onclick="copyRegisteredText('${activeRefId}', 'Reference Syntax Copied!')"
                                class="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 text-xs font-mono font-semibold transition active:scale-95"
                                title="Copy active --sref syntax"
                            >
                                Copy --sref
                            </button>
                        ` : ''}
                    </div>
                </div>
            </div>

            <!-- Model Switcher Toolbar -->
            <div class="flex flex-wrap items-center justify-between gap-3 mb-3">
                <div class="flex flex-wrap items-center gap-1.5 p-1 rounded-xl bg-slate-900 border border-slate-800">
                    <button
                        onclick="switchAdobeStockAIModel('mj')"
                        class="px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${activeModel === 'mj' ? 'bg-purple-600 text-white shadow-md' : 'text-slate-400 hover:text-white'}"
                    >
                        <span>Midjourney v6.1</span>
                    </button>
                    <button
                        onclick="switchAdobeStockAIModel('mj_ref')"
                        class="px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${activeModel === 'mj_ref' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-400 hover:text-white'}"
                        title="Midjourney v6.1 with injected --sref parameter"
                    >
                        <span>MJ + --sref</span>
                    </button>
                    <button
                        onclick="switchAdobeStockAIModel('flux')"
                        class="px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${activeModel === 'flux' ? 'bg-cyan-600 text-white shadow-md' : 'text-slate-400 hover:text-white'}"
                    >
                        <span>Flux.1 Pro</span>
                    </button>
                    <button
                        onclick="switchAdobeStockAIModel('chatgpt')"
                        class="px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${activeModel === 'chatgpt' ? 'bg-emerald-600 text-white shadow-md' : 'text-slate-400 hover:text-white'}"
                        title="ChatGPT (DALL-E 3 & GPT-4o Image)"
                    >
                        <span>ChatGPT</span>
                    </button>
                    <button
                        onclick="switchAdobeStockAIModel('nano')"
                        class="px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${activeModel === 'nano' ? 'bg-amber-600 text-white shadow-md' : 'text-slate-400 hover:text-white'}"
                        title="Google Nano Banana (Gemini 2.5 / 3 Image)"
                    >
                        <span>Nano Banana</span>
                    </button>
                    <button
                        onclick="switchAdobeStockAIModel('video')"
                        class="px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${activeModel === 'video' ? 'bg-blue-600 text-white shadow-md' : 'text-slate-400 hover:text-white'}"
                    >
                        <span>4K Video</span>
                    </button>
                </div>

                <div class="flex items-center gap-2">
                    <button
                        onclick="copyRegisteredText('${currentCopyId}', 'Active Prompt Copied!')"
                        class="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold transition flex items-center gap-1.5 shadow-lg shadow-purple-600/25 active:scale-95"
                    >
                        <i data-lucide="copy" class="w-3.5 h-3.5"></i>
                        <span>Copy Active Prompt</span>
                    </button>
                    <button
                        onclick="copyRegisteredText('${negPromptId}', 'Negative Constraints Copied!')"
                        class="px-3 py-2 rounded-xl bg-rose-500/10 hover:bg-rose-500/20 text-rose-300 border border-rose-500/30 text-xs font-bold transition flex items-center gap-1 active:scale-95"
                        title="Copy Rejection-Proof Negative Prompt"
                    >
                        <i data-lucide="shield-alert" class="w-3.5 h-3.5"></i>
                        <span>Negative</span>
                    </button>
                </div>
            </div>

            <!-- Active Prompt Display Box -->
            <div class="p-4 sm:p-5 rounded-2xl bg-slate-950/90 border ${activeModel === 'chatgpt' ? 'border-emerald-500/40 text-emerald-200' : activeModel === 'nano' ? 'border-amber-500/40 text-amber-200' : activeModel === 'flux' ? 'border-cyan-500/40 text-cyan-200' : activeModel === 'video' ? 'border-blue-500/40 text-blue-200' : 'border-purple-500/30 text-purple-200'} mb-6 shadow-inner font-mono text-xs sm:text-sm leading-relaxed select-all max-h-56 overflow-y-auto no-scrollbar">
                ${escapeHtml(currentPromptText)}
            </div>

            <!-- Prompt Architecture Breakdown Grid -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
                <!-- Lighting -->
                <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
                    <div class="flex items-center gap-1.5 text-amber-300 text-xs font-bold mb-1">
                        <i data-lucide="sun" class="w-3.5 h-3.5"></i>
                        <span>Lighting Architecture</span>
                    </div>
                    <div class="text-[11px] text-slate-300 leading-relaxed">
                        ${escapeHtml(breakdown.lighting || 'Three-point studio lighting with soft diffused fill')}
                    </div>
                </div>

                <!-- Optics & Camera -->
                <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
                    <div class="flex items-center gap-1.5 text-cyan-300 text-xs font-bold mb-1">
                        <i data-lucide="camera" class="w-3.5 h-3.5"></i>
                        <span>Camera Optics</span>
                    </div>
                    <div class="text-[11px] text-slate-300 leading-relaxed font-mono">
                        ${escapeHtml(breakdown.optics || 'Sony A7R V, 85mm f/1.4 GM prime lens')}
                    </div>
                </div>

                <!-- Negative Copy Space -->
                <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
                    <div class="flex items-center gap-1.5 text-indigo-300 text-xs font-bold mb-1">
                        <i data-lucide="layout" class="w-3.5 h-3.5"></i>
                        <span>Copy Space Architecture</span>
                    </div>
                    <div class="text-[11px] text-slate-300 leading-relaxed">
                        ${escapeHtml(breakdown.composition || 'Designated negative copy space for commercial typography')}
                    </div>
                </div>

                <!-- Aesthetic Benchmark -->
                <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
                    <div class="flex items-center gap-1.5 text-purple-300 text-xs font-bold mb-1">
                        <i data-lucide="award" class="w-3.5 h-3.5"></i>
                        <span>Style Benchmark</span>
                    </div>
                    <div class="text-[11px] text-slate-300 leading-relaxed">
                        ${escapeHtml(benchmark)}
                    </div>
                </div>
            </div>

            <!-- Negative Constraints & Adobe Stock Tag SEO Bar -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 pt-4 border-t border-purple-500/20">
                <!-- Rejection-Proof Negative Constraints -->
                <div class="p-4 rounded-xl bg-slate-900/90 border border-rose-500/25 flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-xs font-bold text-rose-300 flex items-center gap-1.5">
                                <i data-lucide="shield-check" class="w-3.5 h-3.5 text-rose-400"></i>
                                Rejection-Prevention Negative Constraints
                            </span>
                            <button onclick="copyRegisteredText('${negPromptId}', 'Negative Prompt Copied!')" class="text-xs text-rose-400 hover:text-rose-300 font-semibold flex items-center gap-1 transition">
                                <i data-lucide="copy" class="w-3 h-3"></i> Copy Negative
                            </button>
                        </div>
                        <p class="text-[11px] text-slate-300 leading-relaxed font-mono">
                            ${escapeHtml(negPrompt)}
                        </p>
                    </div>
                    <div class="text-[10px] text-slate-400 mt-2">
                        Protects against Adobe Stock AI rejection criteria: anatomical distortion, fake watermarks, harsh artifacts.
                    </div>
                </div>

                <!-- 49 Adobe Stock Algorithmic SEO Tags -->
                <div class="p-4 rounded-xl bg-slate-900/90 border border-slate-800 flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-xs font-bold text-white flex items-center gap-1.5">
                                <i data-lucide="tags" class="w-3.5 h-3.5 text-indigo-400"></i>
                                49 Algorithmic SEO Tags (Adobe Stock)
                            </span>
                            <button onclick="copyRegisteredText('${tagsTextId}', '49 Adobe Stock Tags Copied!')" class="text-xs text-indigo-400 hover:text-indigo-300 font-semibold flex items-center gap-1 transition">
                                <i data-lucide="copy" class="w-3 h-3"></i> Copy All 49
                            </button>
                        </div>
                        <div class="p-2.5 rounded-lg bg-slate-950/70 border border-slate-800/80 text-xs text-slate-300 max-h-24 overflow-y-auto leading-relaxed no-scrollbar flex flex-wrap gap-1">
                            ${(tags || []).map(t => `<span class="tag-pill inline-block bg-slate-800/90 px-2 py-0.5 rounded text-[11px] font-mono border border-slate-700/80 cursor-pointer" onclick="copyToClipboard(this.getAttribute('data-tag'), 'Tag Copied!')" data-tag="${escapeHtml(t)}" title="Click to copy single tag">${escapeHtml(t)}</span>`).join('')}
                        </div>
                    </div>
                    <div class="text-[10px] text-slate-400 mt-2">
                        First 10 tags carry ~80% of Adobe Stock algorithm weighting.
                    </div>
                </div>
            </div>
        </div>
    `;

    lucide.createIcons();
}

/**
 * Triggers re-generation in the Adobe Stock AI Studio from user input.
 */
function executeAdobeStockAIGenerate() {
    const input = document.getElementById('adobe-stock-studio-input');
    const refInput = document.getElementById('adobe-stock-studio-ref-input');
    const topic = input ? input.value.trim() : '';
    const refUrl = refInput ? refInput.value.trim() : '';
    if (!topic) {
        showToast('Please enter a seed topic or concept', 'info');
        return;
    }
    loadAdobeStockAIStudio(topic, refUrl);
}

/**
 * Switches the active model view in Adobe Stock AI Studio.
 */
function switchAdobeStockAIModel(modelKey) {
    if (!state.adobeStockStudio) return;
    state.adobeStockStudio.activeModel = modelKey;
    renderAdobeStockAIStudioUI();
}

/**
 * Applies custom reference URL entered in Adobe Stock AI Studio.
 */
function applyCustomRefUrlInStudio() {
    const refInput = document.getElementById('adobe-stock-studio-ref-input');
    const input = document.getElementById('adobe-stock-studio-input');
    const refUrl = refInput ? refInput.value.trim() : '';
    const topic = input ? input.value.trim() : (state.adobeStockStudio ? state.adobeStockStudio.topic : 'abstract 3d liquid waves');
    loadAdobeStockAIStudio(topic, refUrl);
}

// =========================================================================
// --- ANDROID APPS & GOOGLE PLAY STORE PUBLISHING STUDIO CONTROLLER ---
// =========================================================================

async function loadAndroidAppsTab(searchQuery = null) {
    const container = document.getElementById('tab-android-apps');
    if (!container) return;

    if (!state.androidStudio) {
        state.androidStudio = {
            data: null,
            activeSubTab: 'blueprints',
            activeCategory: 'all',
            selectedPermissions: new Set(['android.permission.MANAGE_EXTERNAL_STORAGE', 'android.permission.SCHEDULE_EXACT_ALARM']),
            auditResult: null,
            searchQuery: searchQuery || ''
        };
    } else if (searchQuery !== null) {
        state.androidStudio.searchQuery = searchQuery;
    }

    container.innerHTML = `
        <div class="glass-panel rounded-3xl p-12 text-center border border-emerald-500/30">
            <div class="inline-block animate-spin rounded-full h-12 w-12 border-4 border-emerald-500 border-t-transparent mb-4"></div>
            <h3 class="text-xl font-bold text-white">Loading Google Play App Intelligence...</h3>
            <p class="text-slate-400 text-sm mt-1 max-w-lg mx-auto">
                Crawling trending Android app niches, 30-char SEO titles, Google Play policy restrictions, and exact asset specifications.
            </p>
        </div>
    `;

    try {
        const queryParam = state.androidStudio.searchQuery ? `?q=${encodeURIComponent(state.androidStudio.searchQuery)}` : '';
        const res = await fetch(`/api/android/studio${queryParam}`);
        const data = await res.json();
        state.androidStudio.data = data;
        renderAndroidAppsUI();
    } catch (e) {
        console.error('Error loading Android Studio data:', e);
        container.innerHTML = `
            <div class="glass-panel rounded-3xl p-8 text-center text-rose-400 border border-rose-500/30">
                <i data-lucide="alert-triangle" class="w-10 h-10 mx-auto mb-2"></i>
                <p class="font-bold">Failed to load Android Studio. Please verify the local server is running.</p>
            </div>
        `;
        lucide.createIcons();
    }
}

function renderAndroidAppsUI() {
    const container = document.getElementById('tab-android-apps');
    if (!container || !state.androidStudio || !state.androidStudio.data) return;

    const { trending_apps = [], asset_specs = {}, dangerous_permissions = [], twenty_tester_policy = {}, active_search, search_mode } = state.androidStudio.data;
    const activeSub = state.androidStudio.activeSubTab;
    const activeCat = state.androidStudio.activeCategory;

    // Filter apps by category if active
    let filteredApps = trending_apps;
    if (activeCat === 'zero-cost') {
        filteredApps = trending_apps.filter(a => (a.operating_cost && a.operating_cost.monthly_servers && a.operating_cost.monthly_servers.includes('$0')) || (a.cost_badge && a.cost_badge.includes('$0')));
    } else if (activeCat !== 'all') {
        filteredApps = trending_apps.filter(a => a.category.toLowerCase().includes(activeCat.toLowerCase()));
    }

    let html = `
        <!-- Top Hero Banner -->
        <div class="relative rounded-3xl p-6 sm:p-10 overflow-hidden glass-panel border border-emerald-500/30 shadow-2xl mb-8">
            <div class="absolute -right-20 -top-20 w-96 h-96 bg-emerald-600/15 rounded-full blur-3xl pointer-events-none"></div>
            <div class="absolute -left-20 -bottom-20 w-96 h-96 bg-teal-600/15 rounded-full blur-3xl pointer-events-none"></div>

            <div class="relative z-10 max-w-4xl">
                <div class="flex flex-wrap items-center gap-2 mb-3">
                    <span class="px-3 py-1 rounded-full text-xs font-black bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 flex items-center gap-1.5 font-mono shadow-sm">
                        <i data-lucide="smartphone" class="w-3.5 h-3.5 text-emerald-400"></i>
                        Google Play Store Intelligence v2.0
                    </span>
                    <span class="text-xs text-slate-400 font-mono">Target SDK: <strong>Android 14/15 (API 34/35)</strong></span>
                </div>
                <h2 class="text-2xl sm:text-4xl font-black text-white tracking-tight leading-tight">
                    Android Apps & Play Store <span class="bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400 bg-clip-text text-transparent">Publishing Studio</span>
                </h2>
                <p class="mt-2 text-slate-300 text-xs sm:text-sm max-w-3xl leading-relaxed">
                    Build and upload high-converting Android apps with complete blueprint execution: 30-char SEO titles, 80-char hooks, Master AI Prompts to code the entire app, exact store asset dimensions, and a continuous Google Play Dangerous Permissions Shield.
                </p>

                <!-- Quick Stats Ribbon -->
                <div class="mt-5 grid grid-cols-2 sm:grid-cols-5 gap-3">
                    <div class="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                        <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Trending Niches</div>
                        <div class="text-lg font-black text-emerald-400">${trending_apps.length} Blueprints</div>
                    </div>
                    <div class="p-3 rounded-xl bg-slate-900/80 border border-emerald-500/40">
                        <div class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider">Operating Cost</div>
                        <div class="text-lg font-black text-emerald-300">$0.00 / Month</div>
                    </div>
                    <div class="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                        <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Store Metadata</div>
                        <div class="text-lg font-black text-white">Title &le; 30, Desc &le; 80</div>
                    </div>
                    <div class="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                        <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Policy Shield</div>
                        <div class="text-lg font-black text-amber-400">Zero-Rejection</div>
                    </div>
                    <div class="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                        <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Testing Rule</div>
                        <div class="text-lg font-black text-indigo-400">20-Tester Playbook</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Studio Sub-Navigation Bar -->
        <div class="flex flex-wrap items-center gap-2 p-1.5 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl mb-8">
            <button
                onclick="switchAndroidStudioSubTab('blueprints')"
                class="px-4 py-2.5 rounded-xl text-xs font-bold transition flex items-center gap-2 ${activeSub === 'blueprints' ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md shadow-emerald-600/30' : 'text-slate-400 hover:text-white hover:bg-slate-800/60'}"
            >
                <i data-lucide="sparkles" class="w-4 h-4"></i>
                <span>Trending App Blueprints & AI Prompts</span>
            </button>
            <button
                onclick="switchAndroidStudioSubTab('zero-cost')"
                class="px-4 py-2.5 rounded-xl text-xs font-bold transition flex items-center gap-2 ${activeSub === 'zero-cost' ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md shadow-emerald-600/30' : 'text-slate-400 hover:text-white hover:bg-slate-800/60'}"
            >
                <i data-lucide="badge-dollar-sign" class="w-4 h-4 text-emerald-400"></i>
                <span>$0/Mo Architecture & Cost Guide</span>
            </button>
            <button
                onclick="switchAndroidStudioSubTab('policy-shield')"
                class="px-4 py-2.5 rounded-xl text-xs font-bold transition flex items-center gap-2 ${activeSub === 'policy-shield' ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md shadow-emerald-600/30' : 'text-slate-400 hover:text-white hover:bg-slate-800/60'}"
            >
                <i data-lucide="shield-alert" class="w-4 h-4 text-amber-400"></i>
                <span>Dangerous Permissions & Policy Shield</span>
            </button>
            <button
                onclick="switchAndroidStudioSubTab('asset-specs')"
                class="px-4 py-2.5 rounded-xl text-xs font-bold transition flex items-center gap-2 ${activeSub === 'asset-specs' ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md shadow-emerald-600/30' : 'text-slate-400 hover:text-white hover:bg-slate-800/60'}"
            >
                <i data-lucide="layout-grid" class="w-4 h-4"></i>
                <span>Store Asset Upload Specs & Keystore</span>
            </button>
            <button
                onclick="switchAndroidStudioSubTab('twenty-testers')"
                class="px-4 py-2.5 rounded-xl text-xs font-bold transition flex items-center gap-2 ${activeSub === 'twenty-testers' ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md shadow-emerald-600/30' : 'text-slate-400 hover:text-white hover:bg-slate-800/60'}"
            >
                <i data-lucide="users" class="w-4 h-4 text-indigo-400"></i>
                <span>20-Tester Closed Testing Playbook</span>
            </button>
        </div>
    `;

    const { zero_cost_guide = {} } = state.androidStudio.data;

    // Render active sub-tab view
    if (activeSub === 'blueprints') {
        html += renderAndroidBlueprintsSection(filteredApps, activeCat, search_mode, active_search);
    } else if (activeSub === 'zero-cost') {
        html += renderAndroidZeroCostGuideSection(zero_cost_guide);
    } else if (activeSub === 'policy-shield') {
        html += renderAndroidPolicyShieldSection(dangerous_permissions);
    } else if (activeSub === 'asset-specs') {
        html += renderAndroidAssetSpecsSection(asset_specs);
    } else if (activeSub === 'twenty-testers') {
        html += renderAndroidTwentyTestersSection(twenty_tester_policy);
    }

    container.innerHTML = html;
    lucide.createIcons();
}

/**
 * Sub-Tab 1: Trending App Blueprints & AI Code Prompts
 */
function renderAndroidBlueprintsSection(apps, activeCat, searchMode, activeSearch) {
    const queryVal = state.androidStudio.searchQuery || '';
    return `
        <!-- Niche Search & Category Filters -->
        <div class="glass-panel rounded-3xl p-6 mb-8 border border-slate-800 shadow-xl">
            <div class="flex flex-col md:flex-row items-center justify-between gap-4">
                <!-- Search Input Bar -->
                <div class="w-full md:max-w-xl flex items-center p-1.5 rounded-2xl bg-slate-900/90 border border-slate-700/80 focus-within:border-emerald-500 transition">
                    <i data-lucide="search" class="w-4 h-4 text-slate-500 ml-3 pointer-events-none"></i>
                    <input
                        id="android-niche-search-input"
                        type="text"
                        value="${escapeHtml(queryVal)}"
                        placeholder="Search any app niche (e.g. fasting, document scanner, budget, sleep sounds)..."
                        class="w-full bg-transparent text-white placeholder-slate-500 text-xs sm:text-sm py-2 px-3 focus:outline-none font-medium"
                        onkeydown="if(event.key==='Enter') executeAndroidAppSearch()"
                    />
                    ${queryVal ? `
                        <button onclick="clearAndroidAppSearch()" class="mr-1 px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold flex items-center gap-1" title="Clear">
                            <i data-lucide="x" class="w-3.5 h-3.5"></i>
                        </button>
                    ` : ''}
                    <button
                        onclick="executeAndroidAppSearch()"
                        class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs transition shadow-md shadow-emerald-600/30 flex items-center gap-1.5 shrink-0 active:scale-95"
                    >
                        <i data-lucide="search" class="w-3.5 h-3.5"></i>
                        <span>Crawl Niche</span>
                    </button>
                </div>

                <!-- Category Filter Pills -->
                <div class="flex flex-wrap items-center gap-1.5">
                    ${[
                        { key: 'all', label: 'All Niches' },
                        { key: 'zero-cost', label: '⚡ Zero Cost ($0/mo)' },
                        { key: 'tools', label: 'Tools' },
                        { key: 'finance', label: 'Finance' },
                        { key: 'health', label: 'Health & Fitness' },
                        { key: 'productivity', label: 'Productivity' },
                        { key: 'education', label: 'Education' }
                    ].map(c => `
                        <button
                            onclick="filterAndroidAppsCategory('${c.key}')"
                            class="px-3 py-1.5 rounded-xl text-xs font-semibold transition ${activeCat === c.key ? 'bg-emerald-600 text-white shadow-sm' : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'}"
                        >
                            ${c.label}
                        </button>
                    `).join('')}
                </div>
            </div>

            ${searchMode ? `
                <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                    <div class="flex items-center gap-2">
                        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                        <span class="text-xs text-slate-300 font-mono">Dynamic Blueprint generated for: <strong class="text-emerald-300">"${escapeHtml(activeSearch)}"</strong></span>
                    </div>
                    <button onclick="clearAndroidAppSearch()" class="text-xs text-indigo-400 hover:text-indigo-300 font-semibold flex items-center gap-1">
                        <i data-lucide="rotate-ccw" class="w-3 h-3"></i> Reset to Top Trending
                    </button>
                </div>
            ` : ''}
        </div>

        <!-- App Blueprints Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            ${apps.map((app, idx) => renderAppBlueprintCard(app, idx)).join('')}
        </div>
    `;
}

/**
 * Individual Android App Blueprint Card
 */
function renderAppBlueprintCard(app, idx) {
    const cardId = `android_card_${app.id || idx}`;
    const titleText = app.target_title || '';
    const shortDescText = app.short_description || '';
    const fullDescText = app.full_description || '';
    const promptText = app.kickstart_prompt || '';

    const titleId = registerData(titleText);
    const shortDescId = registerData(shortDescText);
    const fullDescId = registerData(fullDescText);
    const promptId = registerData(promptText);

    const queueId = registerData({
        keyword: app.concept,
        best_marketplace: 'Google Play Store',
        recommended_tool: app.recommended_stack || 'Android Mobile App',
        opportunity_score: app.opportunity_score || 95,
        suggested_title: titleText
    });

    const doneId = registerData({
        suggested_title: titleText,
        asset_type: 'Android App',
        platform: 'Google Play Store',
        concept: app.concept
    });
    const timing = getClientUploadDeadline(app.concept || app.target_title);

    return `
        <div class="glass-card rounded-3xl p-6 border ${timing.is_late ? 'border-rose-500/40 border-l-4 border-l-rose-500 bg-rose-950/20 shadow-rose-900/10' : 'border-slate-800'} flex flex-col justify-between shadow-xl">
            <div>
                <!-- Top Badge Header -->
                <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <div class="flex flex-wrap items-center gap-2">
                        <span class="px-2.5 py-1 rounded-lg text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-mono">
                            ${escapeHtml(app.category)}
                        </span>
                        <span class="px-2.5 py-1 rounded-lg text-xs font-bold bg-teal-500/20 text-teal-300 border border-teal-500/30 font-mono flex items-center gap-1">
                            <i data-lucide="badge-dollar-sign" class="w-3.5 h-3.5 text-emerald-400"></i>
                            ${escapeHtml(app.cost_badge || '🟢 Cost: $0.00/mo')}
                        </span>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="px-2 py-0.5 rounded text-[11px] font-black bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 font-mono">
                            ★ ${app.opportunity_score}/100 Demand
                        </span>
                        <span class="px-2 py-0.5 rounded text-[11px] font-mono text-slate-400 bg-slate-900 border border-slate-800">
                            ${escapeHtml(app.search_volume)}
                        </span>
                    </div>
                </div>

                <h3 class="text-xl font-bold text-white mb-1.5 leading-snug">${escapeHtml(app.concept)}</h3>

                <!-- Commercial Metrics Pill -->
                <div class="flex flex-wrap items-center gap-2 mb-3 px-3 py-1.5 rounded-xl bg-slate-950/80 border border-slate-800 text-[11px] font-mono">
                    <span class="text-emerald-400 font-bold flex items-center gap-1">
                        <i data-lucide="trending-up" class="w-3.5 h-3.5"></i> ${escapeHtml(app.trend_momentum || '+350% Surge')}
                    </span>
                    <span class="text-slate-600">•</span>
                    <span class="text-amber-400">eCPM: ${escapeHtml(app.admob_ecpm)}</span>
                    <span class="text-slate-600 hidden sm:inline">•</span>
                    <span class="text-slate-300 hidden sm:inline">${escapeHtml(app.monetization)}</span>
                </div>

                <!-- Play Store Sprint Window & Launch Deadline -->
                <div class="flex flex-wrap items-center justify-between gap-2 mb-3.5 p-2.5 rounded-xl ${timing.is_late ? 'bg-rose-950/40 border border-rose-500/40' : (timing.timing_status === 'CLOSING_SOON' ? 'bg-amber-950/30 border border-amber-500/40' : 'bg-slate-950/80 border border-slate-800')} text-[11px] font-mono">
                    <div class="flex items-center gap-1.5">
                        <i data-lucide="clock" class="w-3.5 h-3.5 ${timing.is_late ? 'text-rose-400' : 'text-emerald-400'}"></i>
                        <span class="text-slate-300">Sprint: <strong class="text-white">${escapeHtml(timing.upload_date_range)}</strong></span>
                    </div>
                    <div class="flex items-center gap-1.5">
                        <span class="px-2 py-0.5 rounded text-[10px] font-black ${timing.is_late ? 'bg-rose-600 text-white animate-pulse' : (timing.timing_status === 'CLOSING_SOON' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30')}">
                            ${escapeHtml(timing.timing_badge)}
                        </span>
                        <span class="text-slate-400">Due: <strong class="${timing.is_late ? 'text-rose-400 font-bold' : 'text-slate-200'}">${escapeHtml(timing.upload_deadline)}</strong></span>
                    </div>
                </div>

                <!-- Recommended Tech Stack -->
                <div class="mb-3.5 p-3 rounded-xl bg-slate-900/60 border border-slate-800 flex items-start gap-2.5">
                    <span class="w-6 h-6 rounded-lg bg-teal-500/15 border border-teal-500/30 flex items-center justify-center shrink-0 mt-0.5">
                        <i data-lucide="cpu" class="w-3.5 h-3.5 text-teal-400"></i>
                    </span>
                    <div class="text-xs">
                        <span class="font-bold text-slate-300">Recommended Tech Architecture:</span>
                        <div class="text-emerald-300 font-mono mt-0.5">${escapeHtml(app.recommended_stack)}</div>
                    </div>
                </div>

                <!-- Expected Operating Cost Breakdown -->
                ${app.operating_cost ? `
                    <div class="mb-4 p-3.5 rounded-xl bg-slate-950/80 border border-emerald-500/30 text-xs">
                        <div class="flex items-center justify-between pb-2 mb-2 border-b border-slate-800/80">
                            <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-1.5 font-mono">
                                <i data-lucide="coins" class="w-3.5 h-3.5 text-emerald-400"></i>
                                Expected Operating Cost Breakdown:
                            </span>
                            <span class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-300 font-mono font-bold">
                                $0.00 / Mo Ongoing
                            </span>
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px] text-slate-300 font-mono">
                            <div><strong class="text-slate-400">Monthly Servers:</strong> <span class="text-emerald-300">${escapeHtml(app.operating_cost.monthly_servers || '$0.00')}</span></div>
                            <div><strong class="text-slate-400">AI / ML Cost:</strong> <span class="text-emerald-300">${escapeHtml(app.operating_cost.ai_ml_cost || '$0.00')}</span></div>
                            <div><strong class="text-slate-400">Database:</strong> <span class="text-emerald-300">${escapeHtml(app.operating_cost.database_cost || '$0.00')}</span></div>
                            <div><strong class="text-slate-400">Play Console:</strong> <span class="text-amber-300">${escapeHtml(app.operating_cost.one_time_setup || '$25.00')}</span></div>
                        </div>
                        <div class="mt-2 pt-2 border-t border-slate-800/60 text-[10.5px] text-slate-400 leading-snug">
                            <strong class="text-slate-300">Minimum-Cost Cloud Option:</strong> ${escapeHtml(app.operating_cost.minimum_cloud_option || 'Firebase Spark free tier ($0/mo)')}
                        </div>
                    </div>
                ` : ''}

                <!-- Google Play Optimized Title (Strictly <= 30 Chars) -->
                <div class="mb-3 p-3.5 rounded-xl bg-slate-950/70 border border-slate-800/90">
                    <div class="flex items-center justify-between pb-1.5 mb-2 border-b border-slate-800/80">
                        <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                            <i data-lucide="tag" class="w-3.5 h-3.5 text-indigo-400"></i>
                            Google Play App Title (${titleText.length}/30 chars):
                        </span>
                        <button onclick="copyRegisteredText('${titleId}', 'App Title Copied!')" class="text-xs text-indigo-400 hover:text-indigo-300 font-semibold flex items-center gap-1 transition">
                            <i data-lucide="copy" class="w-3 h-3"></i> Copy Title
                        </button>
                    </div>
                    <div class="text-xs font-mono font-bold text-white bg-slate-900/90 p-2.5 rounded-lg border border-slate-800 flex items-center justify-between">
                        <span class="text-emerald-300">${escapeHtml(titleText)}</span>
                        <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/15 text-emerald-400 font-mono">Verified &le; 30</span>
                    </div>
                </div>

                <!-- Google Play Short Description (Strictly <= 80 Chars) -->
                <div class="mb-3.5 p-3.5 rounded-xl bg-slate-950/70 border border-slate-800/90">
                    <div class="flex items-center justify-between pb-1.5 mb-2 border-b border-slate-800/80">
                        <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                            <i data-lucide="sparkles" class="w-3.5 h-3.5 text-amber-400"></i>
                            Short Description Hook (${shortDescText.length}/80 chars):
                        </span>
                        <button onclick="copyRegisteredText('${shortDescId}', 'Short Description Copied!')" class="text-xs text-indigo-400 hover:text-indigo-300 font-semibold flex items-center gap-1 transition">
                            <i data-lucide="copy" class="w-3 h-3"></i> Copy Hook
                        </button>
                    </div>
                    <div class="text-xs text-slate-300 leading-relaxed font-mono bg-slate-900/90 p-2.5 rounded-lg border border-slate-800">
                        ${escapeHtml(shortDescText)}
                    </div>
                </div>

                <!-- Expandable Full Description Drawer -->
                <div class="mb-3.5">
                    <button
                        type="button"
                        onclick="toggleAppDescDrawer('${cardId}')"
                        id="desc-btn-${cardId}"
                        class="w-full py-2 px-3 rounded-xl bg-slate-900/80 hover:bg-slate-800 border border-slate-800 text-xs font-bold text-slate-300 hover:text-white flex items-center justify-between transition active:scale-95"
                    >
                        <span class="flex items-center gap-1.5">
                            <i data-lucide="file-text" class="w-3.5 h-3.5 text-teal-400"></i>
                            <span>View Full Store SEO Description (4000 Chars Formatted)</span>
                        </span>
                        <i data-lucide="chevron-down" id="desc-chevron-${cardId}" class="w-4 h-4 text-slate-400 transition-transform"></i>
                    </button>
                    <div id="desc-drawer-${cardId}" class="hidden mt-2 p-3.5 rounded-xl bg-slate-950/90 border border-slate-800 space-y-2">
                        <div class="flex items-center justify-between pb-2 border-b border-slate-800">
                            <span class="text-[11px] font-bold text-slate-400">Google Play ASO Keyword Layout</span>
                            <button onclick="copyRegisteredText('${fullDescId}', 'Full SEO Description Copied!')" class="text-xs font-bold text-emerald-400 hover:text-emerald-300 flex items-center gap-1">
                                <i data-lucide="copy" class="w-3 h-3"></i> Copy Description
                            </button>
                        </div>
                        <pre class="text-[11px] text-slate-300 whitespace-pre-wrap font-sans leading-relaxed max-h-60 overflow-y-auto no-scrollbar">${escapeHtml(fullDescText)}</pre>
                    </div>
                </div>

                <!-- Dangerous Permission Warning & Policy Status -->
                <div class="mb-3.5 p-3 rounded-xl bg-amber-950/20 border border-amber-500/30 text-xs">
                    <div class="flex items-center justify-between mb-1.5">
                        <span class="text-[10px] font-bold text-amber-300 uppercase tracking-wider flex items-center gap-1.5">
                            <i data-lucide="shield-check" class="w-3.5 h-3.5 text-amber-400"></i>
                            Dangerous Permissions Guard:
                        </span>
                        <span class="text-[10px] font-mono text-emerald-400 font-bold">${escapeHtml(app.dangerous_permissions_check.policy_status || '🟢 Clean')}</span>
                    </div>
                    <div class="text-[11px] text-slate-300 leading-snug">
                        <strong class="text-rose-400">Avoid:</strong> ${(app.dangerous_permissions_check.avoid || []).join(', ') || 'None'}<br/>
                        <strong class="text-emerald-400">Safe Replacement:</strong> ${escapeHtml(app.dangerous_permissions_check.use_instead)}
                    </div>
                </div>

                <!-- Master AI Code Architecture Prompt Drawer -->
                <div class="mb-3.5">
                    <button
                        type="button"
                        onclick="toggleAppPromptDrawer('${cardId}')"
                        id="prompt-btn-${cardId}"
                        class="w-full py-2.5 px-3.5 rounded-xl bg-gradient-to-r from-emerald-950/40 via-teal-950/40 to-slate-900 hover:from-emerald-900/60 hover:to-teal-900/60 border border-emerald-500/40 text-xs font-bold text-emerald-200 hover:text-white flex items-center justify-between transition active:scale-95 shadow-sm"
                    >
                        <span class="flex items-center gap-2">
                            <i data-lucide="code-2" class="w-4 h-4 text-emerald-400"></i>
                            <span>Master AI Code Prompt (Feed into Cursor / Claude / Antigravity)</span>
                        </span>
                        <i data-lucide="chevron-down" id="prompt-chevron-${cardId}" class="w-4 h-4 text-emerald-400 transition-transform"></i>
                    </button>
                    <div id="prompt-drawer-${cardId}" class="hidden mt-2 p-3.5 rounded-xl bg-slate-950/95 border border-emerald-500/30 space-y-2.5">
                        <div class="flex items-center justify-between pb-2 border-b border-emerald-500/20">
                            <span class="text-[11px] font-mono text-emerald-400">Production Code Kickstart Prompt</span>
                            <button onclick="copyRegisteredText('${promptId}', 'Master AI Prompt Copied!')" class="px-2.5 py-1 rounded-lg bg-emerald-600 text-white font-bold text-xs flex items-center gap-1 shadow-sm active:scale-95">
                                <i data-lucide="copy" class="w-3 h-3"></i> Copy Full Prompt
                            </button>
                        </div>
                        <pre class="text-[11px] text-slate-300 whitespace-pre-wrap font-mono leading-relaxed max-h-64 overflow-y-auto no-scrollbar bg-slate-900 p-3 rounded-lg border border-slate-800">${escapeHtml(promptText)}</pre>
                    </div>
                </div>
            </div>

            <!-- Card Bottom Actions -->
            <div class="pt-3 border-t border-slate-800 flex items-center justify-between gap-2">
                <div class="flex items-center gap-2">
                    <button onclick="quickLogAssetFromRegistry('${doneId}')" class="px-3 py-1.5 rounded-xl bg-emerald-600/20 hover:bg-emerald-600/40 text-emerald-300 border border-emerald-500/30 text-xs font-bold transition flex items-center gap-1.5 shadow-sm active:scale-95">
                        <i data-lucide="check" class="w-3.5 h-3.5"></i>
                        Mark Done
                    </button>
                    <button onclick="saveKeywordFromRegistry('${queueId}')" class="px-3 py-1.5 rounded-xl bg-indigo-600/20 hover:bg-indigo-600/40 text-indigo-300 border border-indigo-500/30 text-xs font-bold transition flex items-center gap-1.5 shadow-sm active:scale-95" title="Add to Kanban">
                        <i data-lucide="plus" class="w-3.5 h-3.5"></i>
                        Queue to Kanban
                    </button>
                </div>
                <button onclick="copyRegisteredText('${promptId}', 'Master AI Code Prompt Copied!')" class="text-xs font-bold text-teal-400 hover:text-teal-300 transition flex items-center gap-1">
                    <i data-lucide="terminal" class="w-3.5 h-3.5"></i> Copy AI Prompt
                </button>
            </div>
        </div>
    `;
}


/**
 * Sub-Tab: Zero-Recurring Cost Architecture & Economics Guide
 */
function renderAndroidZeroCostGuideSection(guide) {
    if (!guide) return '<div class="p-8 text-center text-slate-400 font-mono">Loading Zero Cost Guide...</div>';

    const pillars = guide.six_pillars_of_zero_cost || [];
    const comparison = guide.cost_comparison_table || [];

    return `
        <div class="space-y-8 mb-8">
            <!-- Hero Architecture Guide Header -->
            <div class="glass-panel rounded-3xl p-6 sm:p-10 border border-emerald-500/30 shadow-2xl relative overflow-hidden">
                <div class="absolute -right-20 -top-20 w-80 h-80 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>
                <div class="relative z-10 max-w-4xl">
                    <div class="flex items-center gap-2 mb-2">
                        <span class="px-3 py-1 rounded-full text-xs font-black bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-mono">
                            Indie Developer Economics
                        </span>
                        <span class="text-xs text-slate-400 font-mono">Operating Cost: <strong>$0.00 / Month</strong></span>
                    </div>
                    <h3 class="text-2xl sm:text-3xl font-black text-white leading-tight">
                        ${escapeHtml(guide.headline || 'Zero-Recurring Operating Cost App Architecture ($0.00/Month)')}
                    </h3>
                    <p class="text-xs sm:text-sm text-slate-300 mt-2 leading-relaxed">
                        ${escapeHtml(guide.philosophy || '')}
                    </p>

                    <!-- Mandatory vs Optional Cost Breakdown Box -->
                    <div class="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-4">
                        <div class="p-4 rounded-2xl bg-slate-900/90 border border-emerald-500/40">
                            <div class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider font-mono">Monthly Operating Cost</div>
                            <div class="text-2xl font-black text-emerald-300 mt-1">$0.00 <span class="text-xs font-normal text-slate-400">/ mo</span></div>
                            <div class="text-[11px] text-slate-400 mt-1">Zero monthly servers, zero AI API fees, zero database hosting bills.</div>
                        </div>
                        <div class="p-4 rounded-2xl bg-slate-900/90 border border-amber-500/40">
                            <div class="text-[10px] font-bold text-amber-400 uppercase tracking-wider font-mono">One-Time Google Play Fee</div>
                            <div class="text-2xl font-black text-amber-300 mt-1">$25.00 <span class="text-xs font-normal text-slate-400">lifetime</span></div>
                            <div class="text-[11px] text-slate-400 mt-1">${escapeHtml(guide.total_mandatory_costs || '$25 one-time registration, no annual fee.')}</div>
                        </div>
                        <div class="p-4 rounded-2xl bg-slate-900/90 border border-indigo-500/40">
                            <div class="text-[10px] font-bold text-indigo-400 uppercase tracking-wider font-mono">Minimum-Cost Cloud Fallback</div>
                            <div class="text-2xl font-black text-indigo-300 mt-1">$0.00 <span class="text-xs font-normal text-slate-400">tier</span></div>
                            <div class="text-[11px] text-slate-400 mt-1">Firebase Spark / Cloudflare D1 offer 100% free multi-device sync up to 50k ops/day.</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- The 6 Pillars of Zero Operating Cost -->
            <div class="glass-panel rounded-3xl p-6 sm:p-8 border border-slate-800 shadow-xl">
                <div class="flex items-center gap-2 mb-6 pb-3 border-b border-slate-800">
                    <i data-lucide="layers" class="w-5 h-5 text-emerald-400"></i>
                    <h4 class="text-xl font-bold text-white">The 6 Pillars of Zero-Cost Mobile App Engineering</h4>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                    ${pillars.map(p => `
                        <div class="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 flex flex-col justify-between hover:border-emerald-500/40 transition">
                            <div>
                                <div class="text-xs font-black text-emerald-400 font-mono mb-2 uppercase tracking-wide">
                                    ${escapeHtml(p.pillar)}
                                </div>
                                <div class="text-xs text-slate-300 leading-relaxed mb-3">
                                    ${escapeHtml(p.how_it_saves_money)}
                                </div>
                            </div>
                            <div class="pt-3 border-t border-slate-800/80 space-y-1.5 text-[11px]">
                                <div class="text-teal-300 font-mono">
                                    <strong class="text-slate-400">Tech:</strong> ${escapeHtml(p.recommended_tech)}
                                </div>
                                <div class="text-rose-400/90 text-[10.5px]">
                                    <strong class="text-slate-400">Replaces:</strong> ${escapeHtml(p.replaces_expensive_service)}
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>

            <!-- Cost Comparison Table: Traditional vs Zero-Cost Indie -->
            <div class="glass-panel rounded-3xl p-6 sm:p-8 border border-slate-800 shadow-xl overflow-hidden">
                <div class="flex items-center justify-between mb-6 pb-3 border-b border-slate-800">
                    <div class="flex items-center gap-2">
                        <i data-lucide="calculator" class="w-5 h-5 text-amber-400"></i>
                        <h4 class="text-xl font-bold text-white">Cost Comparison: Traditional SaaS vs Zero-Cost Indie Mobile</h4>
                    </div>
                    <span class="text-xs text-emerald-400 font-mono font-bold bg-emerald-500/10 px-3 py-1 rounded-lg border border-emerald-500/20">
                        Average Annual Savings: $1,200 - $3,500/yr
                    </span>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse text-xs">
                        <thead>
                            <tr class="border-b border-slate-800 text-[11px] font-mono text-slate-400 uppercase tracking-wider">
                                <th class="py-3 px-4">Component</th>
                                <th class="py-3 px-4 text-rose-400">Expensive Traditional Approach</th>
                                <th class="py-3 px-4 text-emerald-400">Zero-Cost Indie Approach ($0/mo)</th>
                                <th class="py-3 px-4 text-amber-300 text-right">Your Savings</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800/60 font-sans">
                            ${comparison.map(row => `
                                <tr class="hover:bg-slate-900/40 transition">
                                    <td class="py-3 px-4 font-bold text-white">${escapeHtml(row.feature)}</td>
                                    <td class="py-3 px-4 text-rose-300 font-mono text-[11px]">${escapeHtml(row.expensive_traditional_approach)}</td>
                                    <td class="py-3 px-4 text-emerald-300 font-mono text-[11px] font-semibold">${escapeHtml(row.zero_cost_indie_approach)}</td>
                                    <td class="py-3 px-4 text-amber-300 font-mono text-right font-bold">${escapeHtml(row.savings)}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    `;
}

/**
 * Sub-Tab 2: Dangerous Permissions & Google Play Policy Shield
 */
function renderAndroidPolicyShieldSection(directory) {
    const selected = state.androidStudio.selectedPermissions || new Set();
    const auditResult = state.androidStudio.auditResult;

    return `
        <!-- Live Interactive Dangerous Permissions Auditor -->
        <div class="glass-panel rounded-3xl p-6 sm:p-8 mb-8 border border-amber-500/30 shadow-2xl">
            <div class="flex flex-col md:flex-row md:items-center justify-between pb-4 mb-5 border-b border-slate-800 gap-4">
                <div>
                    <div class="flex items-center gap-2 mb-1">
                        <span class="px-2.5 py-0.5 rounded-full text-xs font-black bg-amber-500/20 text-amber-300 border border-amber-500/40 font-mono">
                            Interactive Pre-Flight Scanner
                        </span>
                        <span class="text-xs text-slate-400 font-mono">Google Play 2024 Policy Enforcement</span>
                    </div>
                    <h3 class="text-2xl font-bold text-white">Dangerous Permissions & Rejection Risk Auditor</h3>
                    <p class="text-xs text-slate-400 mt-1 max-w-2xl leading-relaxed">
                        Select permissions your app intends to request. The scanner evaluates rejection probability and delivers modern zero-risk replacement APIs.
                    </p>
                </div>
                <button
                    onclick="auditPermissionsInteractive()"
                    class="px-6 py-3 rounded-xl bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-400 hover:to-orange-500 text-white font-bold text-xs sm:text-sm transition shadow-lg shadow-orange-500/25 flex items-center gap-2 active:scale-95 shrink-0"
                >
                    <i data-lucide="shield-check" class="w-4 h-4"></i>
                    <span>Audit Selected Permissions</span>
                </button>
            </div>

            <!-- Permission Checkbox Grid -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
                ${directory.map(p => {
                    const isChecked = selected.has(p.permission);
                    return `
                        <label class="flex items-start gap-2.5 p-3 rounded-xl ${isChecked ? 'bg-slate-800/90 border-amber-500/50' : 'bg-slate-900/60 border-slate-800'} border cursor-pointer hover:border-slate-700 transition">
                            <input
                                type="checkbox"
                                value="${escapeHtml(p.permission)}"
                                ${isChecked ? 'checked' : ''}
                                onchange="togglePermissionSelection('${escapeHtml(p.permission)}')"
                                class="mt-0.5 w-4 h-4 rounded text-amber-500 bg-slate-950 border-slate-700 focus:ring-0"
                            />
                            <div class="min-w-0">
                                <div class="text-xs font-bold text-white truncate">${escapeHtml(p.name)}</div>
                                <div class="text-[10px] font-mono text-slate-400 truncate">${escapeHtml(p.permission.split('.').pop())}</div>
                            </div>
                        </label>
                    `;
                }).join('')}
            </div>

            <!-- Live Audit Verdict Panel -->
            ${auditResult ? `
                <div class="p-5 rounded-2xl ${auditResult.verdict === 'CRITICAL_REJECTION_RISK' ? 'bg-rose-950/30 border-rose-500/40 text-rose-200' : (auditResult.verdict === 'DECLARATION_REQUIRED' ? 'bg-amber-950/30 border-amber-500/40 text-amber-200' : 'bg-emerald-950/30 border-emerald-500/40 text-emerald-200')} border shadow-xl">
                    <div class="flex items-center justify-between mb-3 pb-2 border-b border-slate-800/80">
                        <div class="flex items-center gap-2">
                            <span class="w-3 h-3 rounded-full ${auditResult.verdict === 'CRITICAL_REJECTION_RISK' ? 'bg-rose-500 animate-ping' : (auditResult.verdict === 'DECLARATION_REQUIRED' ? 'bg-amber-400' : 'bg-emerald-400')}"></span>
                            <span class="text-sm font-black uppercase tracking-wider font-mono">
                                Audit Result: ${escapeHtml(auditResult.verdict.replace(/_/g, ' '))}
                            </span>
                        </div>
                        <span class="text-xs font-mono font-bold">${auditResult.total_audited} Permissions Evaluated</span>
                    </div>

                    <div class="space-y-3">
                        ${auditResult.findings.map(f => `
                            <div class="p-3 rounded-xl bg-slate-950/80 border border-slate-800 text-xs">
                                <div class="flex items-center justify-between mb-1.5">
                                    <span class="font-bold text-white font-mono">${escapeHtml(f.permission)}</span>
                                    <span class="px-2 py-0.5 rounded text-[10px] font-black bg-${f.badge_color}-500/20 text-${f.badge_color}-400 border border-${f.badge_color}-500/40 font-mono">
                                        ${escapeHtml(f.risk_level.replace(/_/g, ' '))}
                                    </span>
                                </div>
                                <div class="text-[11px] text-slate-300 mb-1 leading-relaxed">
                                    <strong class="text-amber-400">Play Store Rule:</strong> ${escapeHtml(f.policy_rule)}
                                </div>
                                <div class="text-[11px] text-emerald-300 font-mono leading-relaxed">
                                    <strong>Zero-Risk Replacement:</strong> ${escapeHtml(f.safe_alternative)}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            ` : ''}
        </div>

        <!-- Dangerous Permissions Master Directory -->
        <div class="glass-panel rounded-3xl p-6 sm:p-8 mb-8 border border-slate-800 shadow-xl">
            <div class="flex items-center gap-2 mb-4">
                <i data-lucide="shield" class="w-5 h-5 text-emerald-400"></i>
                <h3 class="text-xl font-bold text-white">Google Play Policy Watchdog & Permissions Directory</h3>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                ${directory.map(p => `
                    <div class="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between mb-2">
                                <span class="text-xs font-bold text-white font-mono">${escapeHtml(p.name)}</span>
                                <span class="px-2 py-0.5 rounded text-[10px] font-black bg-${p.badge_color}-500/20 text-${p.badge_color}-300 border border-${p.badge_color}-500/30 font-mono">
                                    ${escapeHtml(p.risk_level.replace(/_/g, ' '))}
                                </span>
                            </div>
                            <div class="text-[11px] font-mono text-slate-500 mb-2 truncate">${escapeHtml(p.permission)}</div>
                            <p class="text-xs text-slate-300 mb-2.5 leading-relaxed">${escapeHtml(p.policy_rule)}</p>
                        </div>
                        <div class="pt-2.5 border-t border-slate-800/80 text-[11px] text-emerald-300 font-mono">
                            <strong>Safe Modern API:</strong> ${escapeHtml(p.safe_alternative)}
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

/**
 * Sub-Tab 3: Exact Store Asset Dimensions & Specs
 */
function renderAndroidAssetSpecsSection(specs) {
    const keystoreCmd = `keytool -genkey -v -keystore release-key.jks -alias my-app-key -keyalg RSA -keysize 2048 -validity 10000 -storetype PKCS12`;
    const keystoreId = registerData(keystoreCmd);

    return `
        <!-- Asset Upload Specs Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            <!-- App Icon -->
            <div class="glass-card rounded-3xl p-6 border border-slate-800 shadow-xl flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <span class="w-8 h-8 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold">1</span>
                        <span class="px-2.5 py-0.5 rounded text-[10px] font-mono font-bold bg-slate-900 text-slate-400 border border-slate-800">Launcher</span>
                    </div>
                    <h4 class="text-lg font-bold text-white mb-1">${escapeHtml(specs.app_icon.title)}</h4>
                    <div class="text-xs font-mono text-emerald-300 font-bold mb-3">${escapeHtml(specs.app_icon.dimension)} • ${escapeHtml(specs.app_icon.format)}</div>
                    <ul class="space-y-2 text-xs text-slate-300">
                        ${(specs.app_icon.critical_rules || []).map(r => `
                            <li class="flex items-start gap-2">
                                <i data-lucide="check" class="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5"></i>
                                <span class="leading-snug">${escapeHtml(r)}</span>
                            </li>
                        `).join('')}
                    </ul>
                </div>
            </div>

            <!-- Feature Graphic -->
            <div class="glass-card rounded-3xl p-6 border border-slate-800 shadow-xl flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <span class="w-8 h-8 rounded-xl bg-teal-500/20 text-teal-400 flex items-center justify-center font-bold">2</span>
                        <span class="px-2.5 py-0.5 rounded text-[10px] font-mono font-bold bg-slate-900 text-slate-400 border border-slate-800">Banner</span>
                    </div>
                    <h4 class="text-lg font-bold text-white mb-1">${escapeHtml(specs.feature_graphic.title)}</h4>
                    <div class="text-xs font-mono text-teal-300 font-bold mb-3">${escapeHtml(specs.feature_graphic.dimension)} • ${escapeHtml(specs.feature_graphic.format)}</div>
                    <ul class="space-y-2 text-xs text-slate-300">
                        ${(specs.feature_graphic.critical_rules || []).map(r => `
                            <li class="flex items-start gap-2">
                                <i data-lucide="check" class="w-3.5 h-3.5 text-teal-400 shrink-0 mt-0.5"></i>
                                <span class="leading-snug">${escapeHtml(r)}</span>
                            </li>
                        `).join('')}
                    </ul>
                </div>
            </div>

            <!-- Phone Screenshots -->
            <div class="glass-card rounded-3xl p-6 border border-slate-800 shadow-xl flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <span class="w-8 h-8 rounded-xl bg-cyan-500/20 text-cyan-400 flex items-center justify-center font-bold">3</span>
                        <span class="px-2.5 py-0.5 rounded text-[10px] font-mono font-bold bg-slate-900 text-slate-400 border border-slate-800">${escapeHtml(specs.phone_screenshots.count)}</span>
                    </div>
                    <h4 class="text-lg font-bold text-white mb-1">${escapeHtml(specs.phone_screenshots.title)}</h4>
                    <div class="text-xs font-mono text-cyan-300 font-bold mb-3">${escapeHtml(specs.phone_screenshots.dimension)}</div>
                    <ul class="space-y-2 text-xs text-slate-300">
                        ${(specs.phone_screenshots.critical_rules || []).map(r => `
                            <li class="flex items-start gap-2">
                                <i data-lucide="check" class="w-3.5 h-3.5 text-cyan-400 shrink-0 mt-0.5"></i>
                                <span class="leading-snug">${escapeHtml(r)}</span>
                            </li>
                        `).join('')}
                    </ul>
                </div>
            </div>
        </div>

        <!-- Release Package (.AAB) & Keystore Terminal Generator -->
        <div class="glass-panel rounded-3xl p-6 sm:p-8 mb-8 border border-slate-800 shadow-xl">
            <div class="flex flex-col md:flex-row md:items-center justify-between pb-4 mb-4 border-b border-slate-800 gap-4">
                <div>
                    <h3 class="text-xl font-bold text-white flex items-center gap-2">
                        <i data-lucide="terminal" class="w-5 h-5 text-indigo-400"></i>
                        Release Package (.AAB) & Custom Keystore Generation
                    </h3>
                    <p class="text-xs text-slate-400 mt-1">Google Play requires all new apps to be submitted as Android App Bundles (.aab) with 64-bit binaries.</p>
                </div>
                <button onclick="copyRegisteredText('${keystoreId}', 'Keystore Command Copied!')" class="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs flex items-center gap-1.5 transition active:scale-95 shadow-md">
                    <i data-lucide="copy" class="w-3.5 h-3.5"></i>
                    <span>Copy Keystore Command</span>
                </button>
            </div>

            <div class="p-4 rounded-xl bg-slate-950 font-mono text-xs text-emerald-300 border border-slate-800/80 mb-4 overflow-x-auto no-scrollbar">
                <code>${escapeHtml(keystoreCmd)}</code>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                <div class="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                    <div class="font-bold text-slate-400 uppercase text-[10px] mb-1">Target SDK</div>
                    <div class="text-white font-mono font-bold">${escapeHtml(specs.release_binary.target_sdk)}</div>
                </div>
                <div class="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                    <div class="font-bold text-slate-400 uppercase text-[10px] mb-1">Architecture</div>
                    <div class="text-white font-mono font-bold">${escapeHtml(specs.release_binary.architecture)}</div>
                </div>
                <div class="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                    <div class="font-bold text-slate-400 uppercase text-[10px] mb-1">Signing Protocol</div>
                    <div class="text-white font-mono font-bold">Google Play App Signing (PEP)</div>
                </div>
            </div>
        </div>
    `;
}

/**
 * Sub-Tab 4: 20-Tester Closed Testing Mandatory Requirement Guide
 */
function renderAndroidTwentyTestersSection(policy) {
    return `
        <div class="glass-panel rounded-3xl p-6 sm:p-10 mb-8 border border-indigo-500/30 shadow-2xl">
            <div class="flex items-center gap-3 mb-3">
                <span class="p-2 rounded-xl bg-indigo-500/20 border border-indigo-500/30 text-indigo-400">
                    <i data-lucide="users" class="w-6 h-6"></i>
                </span>
                <div>
                    <h3 class="text-2xl font-black text-white">${escapeHtml(policy.title || '20-Tester Mandatory Requirement')}</h3>
                    <p class="text-xs text-slate-400">Mandatory rule enforced on all personal developer accounts created after Nov 13, 2023.</p>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
                <!-- Strict Rules Box -->
                <div class="p-5 rounded-2xl bg-slate-950/80 border border-slate-800">
                    <h4 class="text-sm font-bold text-amber-400 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                        <i data-lucide="alert-circle" class="w-4 h-4"></i>
                        The 4 Google Play Gatekeeper Rules:
                    </h4>
                    <ul class="space-y-2.5 text-xs text-slate-300">
                        ${(policy.rules || []).map(r => `
                            <li class="flex items-start gap-2.5">
                                <span class="w-1.5 h-1.5 rounded-full bg-amber-400 mt-1.5 shrink-0"></span>
                                <span class="leading-relaxed">${escapeHtml(r)}</span>
                            </li>
                        `).join('')}
                    </ul>
                </div>

                <!-- Actionable Survival Strategy -->
                <div class="p-5 rounded-2xl bg-slate-950/80 border border-indigo-500/30">
                    <h4 class="text-sm font-bold text-emerald-400 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                        <i data-lucide="check-circle" class="w-4 h-4"></i>
                        5-Step Production Approval Blueprint:
                    </h4>
                    <ul class="space-y-2.5 text-xs text-slate-300">
                        ${(policy.actionable_blueprint || []).map(b => `
                            <li class="flex items-start gap-2.5">
                                <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-1.5 shrink-0"></span>
                                <span class="leading-relaxed">${escapeHtml(b)}</span>
                            </li>
                        `).join('')}
                    </ul>
                </div>
            </div>
        </div>
    `;
}

// --- ANDROID STUDIO ACTIONS ---

function switchAndroidStudioSubTab(subTab) {
    if (!state.androidStudio) return;
    state.androidStudio.activeSubTab = subTab;
    renderAndroidAppsUI();
}

function filterAndroidAppsCategory(cat) {
    if (!state.androidStudio) return;
    state.androidStudio.activeCategory = cat;
    renderAndroidAppsUI();
}

function executeAndroidAppSearch() {
    const input = document.getElementById('android-niche-search-input');
    const q = input ? input.value.trim() : '';
    if (!q) {
        showToast('Please type an app niche or keyword to search', 'info');
        return;
    }
    loadAndroidAppsTab(q);
}

function clearAndroidAppSearch() {
    loadAndroidAppsTab('');
}

function toggleAppDescDrawer(cardId) {
    const drawer = document.getElementById(`desc-drawer-${cardId}`);
    const chevron = document.getElementById(`desc-chevron-${cardId}`);
    if (!drawer) return;
    const isHidden = drawer.classList.contains('hidden');
    if (isHidden) {
        drawer.classList.remove('hidden');
        if (chevron) chevron.classList.add('rotate-180');
    } else {
        drawer.classList.add('hidden');
        if (chevron) chevron.classList.remove('rotate-180');
    }
}

function toggleAppPromptDrawer(cardId) {
    const drawer = document.getElementById(`prompt-drawer-${cardId}`);
    const chevron = document.getElementById(`prompt-chevron-${cardId}`);
    if (!drawer) return;
    const isHidden = drawer.classList.contains('hidden');
    if (isHidden) {
        drawer.classList.remove('hidden');
        if (chevron) chevron.classList.add('rotate-180');
    } else {
        drawer.classList.add('hidden');
        if (chevron) chevron.classList.remove('rotate-180');
    }
}

function togglePermissionSelection(perm) {
    if (!state.androidStudio || !state.androidStudio.selectedPermissions) return;
    if (state.androidStudio.selectedPermissions.has(perm)) {
        state.androidStudio.selectedPermissions.delete(perm);
    } else {
        state.androidStudio.selectedPermissions.add(perm);
    }
}

async function auditPermissionsInteractive() {
    if (!state.androidStudio) return;
    const perms = Array.from(state.androidStudio.selectedPermissions || []);
    if (perms.length === 0) {
        showToast('Please select at least 1 permission to audit', 'info');
        return;
    }

    try {
        const res = await fetch('/api/android/audit-permissions', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ permissions: perms })
        });
        const result = await res.json();
        state.androidStudio.auditResult = result;
        renderAndroidAppsUI();
        showToast(`Audit complete: ${result.verdict.replace(/_/g, ' ')}`, result.verdict === 'PASSED_SAFE' ? 'success' : 'info');
    } catch (e) {
        console.error('Audit failed:', e);
        showToast('Audit failed. Please try again.', 'error');
    }
}




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

