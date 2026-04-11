// Morning Brief - 프론트엔드 렌더러
// data.json을 읽어 섹션별 카드로 그린다.

const SECTIONS = ["world", "tech", "startup", "videos"];

function fmtDate(iso) {
  if (!iso) return "";
  try {
    const d = new Date(iso);
    return d.toLocaleString("ko-KR", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return "";
  }
}

function todayLabel() {
  const d = new Date();
  return d.toLocaleDateString("ko-KR", {
    year: "numeric",
    month: "long",
    day: "numeric",
    weekday: "long",
  });
}

function escapeHtml(s) {
  return (s || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function articleCard(item) {
  return `
    <a href="${escapeHtml(item.url)}" target="_blank" rel="noopener" class="card rounded-xl p-4 block">
      <div class="flex items-center gap-2 mb-2">
        <span class="chip text-[11px] px-2 py-0.5 rounded-full">${escapeHtml(item.source)}</span>
        <span class="text-[11px] text-[#5b6378]">${fmtDate(item.published)}</span>
      </div>
      <h3 class="text-[15px] font-semibold leading-snug mb-1.5">${escapeHtml(item.title)}</h3>
      <p class="text-[13px] text-[#8a92a6] leading-relaxed line-clamp-2">${escapeHtml(item.summary)}</p>
    </a>
  `;
}

function videoCard(item) {
  const thumb = item.thumbnail
    ? `<img src="${escapeHtml(item.thumbnail)}" alt="" class="w-full aspect-video object-cover rounded-lg mb-3" loading="lazy" />`
    : `<div class="w-full aspect-video rounded-lg mb-3 bg-[#1a1f2e]"></div>`;
  return `
    <a href="${escapeHtml(item.url)}" target="_blank" rel="noopener" class="card rounded-xl p-3 block">
      ${thumb}
      <div class="flex items-center gap-2 mb-1">
        <span class="chip text-[11px] px-2 py-0.5 rounded-full">${escapeHtml(item.source)}</span>
        <span class="text-[11px] text-[#5b6378]">${fmtDate(item.published)}</span>
      </div>
      <h3 class="text-[14px] font-semibold leading-snug">${escapeHtml(item.title)}</h3>
    </a>
  `;
}

function skeleton(n, kind) {
  const cls = kind === "video" ? "aspect-video" : "h-24";
  return Array.from({ length: n })
    .map(() => `<div class="card rounded-xl p-4"><div class="${cls} skeleton rounded"></div></div>`)
    .join("");
}

const EMPTY_HINT = {
  videos: "YOUTUBE_API_KEY 가 설정되지 않아 영상이 없어요. README 를 참고해 키를 등록해 주세요.",
  world: "이 카테고리에 항목이 없어요.",
  tech: "이 카테고리에 항목이 없어요.",
  startup: "이 카테고리에 항목이 없어요.",
};

function renderSection(name, items) {
  const sec = document.querySelector(`[data-section="${name}"] [data-grid]`);
  if (!sec) return;
  if (!items || items.length === 0) {
    sec.innerHTML = `<p class="text-sm text-[#5b6378] col-span-full">${EMPTY_HINT[name] || "아직 데이터가 없어요."}</p>`;
    return;
  }
  const isVideo = name === "videos";
  sec.innerHTML = items.map(isVideo ? videoCard : articleCard).join("");
}

async function load() {
  document.getElementById("date").textContent = todayLabel();
  // 스켈레톤 먼저
  for (const name of SECTIONS) {
    const sec = document.querySelector(`[data-section="${name}"] [data-grid]`);
    sec.innerHTML = skeleton(name === "videos" ? 6 : 4, name === "videos" ? "video" : "article");
  }

  try {
    const res = await fetch(`./data.json?t=${Date.now()}`, { cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    document.getElementById("updated").textContent = fmtDate(data.generated_at) || "—";
    for (const name of SECTIONS) {
      renderSection(name, data.sections?.[name] || []);
    }
  } catch (e) {
    console.error(e);
    for (const name of SECTIONS) {
      const sec = document.querySelector(`[data-section="${name}"] [data-grid]`);
      sec.innerHTML = `<p class="text-sm text-red-400 col-span-full">데이터를 불러오지 못했어요: ${escapeHtml(e.message)}</p>`;
    }
  }
}

load();
