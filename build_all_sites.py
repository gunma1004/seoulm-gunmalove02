import os
import random
from string import Template

# 기본 도메인 주소 (본인의 Netlify 주소로 필요시 수정 가능)
BASE_URL = "https://seoulm-gunmalove02.netlify.app"

# 서울시 주요 자치구 및 동 데이터베이스
regions = {
    "gangnamgu": {
        "name": "강남구",
        "intro": "테헤란로 중심의 오피스 밀집 지역과 코엑스, 신사동 가로수길, 압구정 로데오 등 주요 상권이 어우러진 강남구 전 지역은 바쁜 일상 속 직장인들과 주민들의 피로 누적이 심한 곳입니다.",
        "dongs": [
            {"name": "신사동", "slug": "sinsadong"},
            {"name": "논현동", "slug": "nonhyeondong"},
            {"name": "삼성동", "slug": "samseongdong"},
            {"name": "대치동", "slug": "daechidong"},
            {"name": "역삼동", "slug": "yeoksamdong"},
            {"name": "도곡동", "slug": "dogokdong"},
            {"name": "개포동", "slug": "gaepodong"},
            {"name": "일원동", "slug": "ilwondong"},
            {"name": "수서동", "slug": "suseodong"},
            {"name": "압구정동", "slug": "apgujeongdong"},
            {"name": "청담동", "slug": "cheongdamdong"}
        ]
    },
    "gangseogu": {
        "name": "강서구",
        "intro": "마곡지구 첨단 R&D 산업단지와 화곡동, 발산역 주변 대규모 주거 상권이 활기를 띠는 강서구는 직장인과 주거민의 1인 가구 비율이 높아 프라이빗한 홈케어 수요가 매우 높습니다.",
        "dongs": [
            {"name": "화곡동", "slug": "hwagokdong"},
            {"name": "마곡동", "slug": "magokdong"},
            {"name": "가양동", "slug": "gayangdong"},
            {"name": "등촌동", "slug": "deungchondong"},
            {"name": "방화동", "slug": "banghwadong"},
            {"name": "염창동", "slug": "yeomchangdong"}
        ]
    },
    "mapogu": {
        "name": "마포구",
        "intro": "홍대입구와 합정동의 활기찬 문화 상권부터 상암DMC 업무 지구, 연남동과 망원동의 라이프스타일이 공존하는 마포구는 언제나 활력이 넘치지만 그만큼 피로도 쉽게 쌓이는 지역입니다.",
        "dongs": [
            {"name": "합정동", "slug": "hapjeongdong"},
            {"name": "서교동", "slug": "seogyodong"},
            {"name": "상암동", "slug": "sangamdong"},
            {"name": "망원동", "slug": "mangwondong"},
            {"name": "연남동", "slug": "yeonnamdong"},
            {"name": "공덕동", "slug": "gongdeokdong"},
            {"name": "용강동", "slug": "yonggangdong"},
            {"name": "성산동", "slug": "seongsandong"}
        ]
    },
    "songpagu": {
        "name": "송파구",
        "intro": "잠실 롯데월드타워와 석촌호수 중심의 대규모 상권, 방이동 먹자골목 및 문정동 법조단지가 어우러진 송파구는 서울 동남권의 핵심 주거·업무 중심지입니다.",
        "dongs": [
            {"name": "잠실동", "slug": "jamsildong"},
            {"name": "방이동", "slug": "bangidong"},
            {"name": "문정동", "slug": "munjeongdong"},
            {"name": "가락동", "slug": "garakdong"},
            {"name": "석촌동", "slug": "seokchondong"},
            {"name": "오금동", "slug": "ogeumdong"},
            {"name": "거여동", "slug": "geoyeodong"},
            {"name": "마천동", "slug": "macheondong"}
        ]
    }
}

# 공통 깔끔 스타일
common_style = """
:root {--p:#8a1f34; --a:#c98a6a; --bg:#faf6f1; --bg2:#ffffff; --txt:#2a1418; --muted:#7a5c60; --bdr:#e8dcd2; --hd:#fff; --ft:#1e0d11; }
* { box-sizing:border-box; margin:0; padding:0; }
body { background:var(--bg); color:var(--txt); font-family:'Pretendard',sans-serif; line-height:1.7; }
a { color:inherit; text-decoration:none; }
.cm2-hd { background:var(--hd); border-bottom:2px solid var(--p); position:sticky; top:0; z-index:100; }
.cm2-hd-inner { max-width:1100px; margin:0 auto; display:flex; align-items:center; justify-content:space-between; height:62px; padding:0 20px; }
.cm2-logo-text { font-size:16px; font-weight:800; color:var(--p); }
.cm2-sec { padding:44px 20px; }
.cm2-sec-inner { max-width:1100px; margin:0 auto; }
.cm2-sec-hd { margin-bottom:22px; }
.cm2-sec-hd h2 { font-size:21px; font-weight:800; color:var(--p); position:relative; padding-left:12px; border-left:4px solid var(--p); }
.cm2-page-h1 { font-size:24px; font-weight:900; color:var(--p); line-height:1.3; margin-bottom:8px; }
.cm2-sec-sub { font-size:14px; color:var(--muted); margin-top:4px; }
.cm2-bc { background:#fff; border-bottom:1px solid var(--bdr); padding:10px 20px; }
.cm2-bc-inner { max-width:1100px; margin:0 auto; font-size:12px; color:#5a3f36; }
.cm2-dong-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(130px,1fr)); gap:8px; }
.cm2-dong-card { background:#fff; border:1.5px solid var(--bdr); border-radius:8px; padding:12px 14px; text-align:center; display:block; transition:all .15s; }
.cm2-dong-card:hover { border-color:var(--p); background:#eef3fa; }
.cm2-dong-card strong { display:block; font-size:14px; font-weight:700; color:var(--txt); }
.cm2-dong-card span { font-size:11px; color:var(--muted); }
.cm2-price-tbl { width:100%; border-collapse:collapse; font-size:14px; margin-top:10px; }
.cm2-price-tbl th { background:var(--p); color:#fff; padding:12px 14px; text-align:left; font-weight:700; }
.cm2-price-tbl td { padding:12px 14px; border-bottom:1px solid var(--bdr); color:var(--txt); background:#fff; }
.cm2-price-tbl tr:nth-child(even) td { background:#fcf8f5; }
.cm2-step-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:14px; margin-top:15px; }
.cm2-step-card { background:#fff; border:1px solid var(--bdr); border-radius:10px; padding:20px; box-shadow:0 2px 6px rgba(0,0,0,0.02); }
.cm2-step-card strong { display:block; font-size:16px; color:var(--p); margin-bottom:6px; }
.cm2-step-card p { font-size:13px; color:var(--muted); line-height:1.6; }
.cm2-faq details { border:1.5px solid var(--bdr); border-radius:8px; overflow:hidden; background:#fff; margin-bottom:10px; }
.cm2-faq summary { padding:16px; font-size:15px; font-weight:700; cursor:pointer; color:var(--txt); }
.cm2-faq p { padding:0 16px 16px; font-size:14px; color:var(--muted); line-height:1.7; }
.cm2-shop-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:14px; margin-top:10px; }
.cm2-shop-card { background:#fff; border:1px solid var(--bdr); border-radius:8px; padding:16px; box-shadow:0 2px 4px rgba(0,0,0,0.02); }
.cm2-shop-card strong { font-size:15px; color:var(--txt); display:block; margin-bottom:4px; }
.cm2-shop-phone { font-size:15px; font-weight:800; color:var(--p); margin:8px 0 12px; display:block; }
.cm2-btn-group { display:flex; gap:6px; }
.cm2-btn-call { flex:1; background:var(--p); color:#fff; text-align:center; padding:10px; border-radius:6px; font-size:13px; font-weight:700; text-decoration:none; }
.cm2-btn-sms { flex:1; background:#c98a6a; color:#fff; text-align:center; padding:10px; border-radius:6px; font-size:13px; font-weight:700; text-decoration:none; }
.cm2-ft { background:var(--ft); padding:40px 20px; color:#8fa4be; text-align:center; font-size:13px; margin-top:40px; }
"""

shops_script = """
<script>
  const shops = [
    { name: "한국미인테라피", tel: "0507-1280-3201", desc: "엄선된 전문 관리사의 정성스러운 1:1 맞춤 방문 케어 서비스." },
    { name: "오늘밤테라피", tel: "0507-1280-3199", desc: "지친 일상에 편안한 휴식을 선사하는 프리미엄 힐링 프로그램." },
    { name: "주주테라피", tel: "0507-1280-3197", desc: "신속한 방문과 부드러운 이완을 도와주는 전문 홈케어 제휴샵." },
    { name: "한국골든테라피", tel: "0507-1280-3360", desc: "고객 맞춤형 강도 조절과 깊은 피로 회복을 위한 힐링 공간." },
    { name: "퀸즈홈테라피", tel: "0507-1280-3296", desc: "프라이빗하고 품격 있는 케어로 지친 몸과 마음을 달래드립니다." }
  ];

  function shuffleArray(arr) {
    return [...arr].sort(() => 0.5 - Math.random());
  }

  window.addEventListener('DOMContentLoaded', () => {
    const shopContainer = document.getElementById('random-shop-list');
    if(!shopContainer) return;
    const shuffledShops = shuffleArray(shops);
    let shopHtml = '';
    shuffledShops.forEach(shop => {
      shopHtml += `
        <div class="cm2-shop-card">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
            <strong>${shop.name}</strong>
            <span style="background:#fff9ee;border:1px solid #e8c87a;color:#8a6000;padding:2px 6px;border-radius:4px;font-size:11px;font-weight:700;">★ 제휴점</span>
          </div>
          <p style="font-size:13px;color:var(--muted);line-height:1.5;margin-bottom:8px;">${shop.desc}</p>
          <span class="cm2-shop-phone">📞 ${shop.tel}</span>
          <div class="cm2-btn-group">
            <a href="tel:${shop.tel}" class="cm2-btn-call">📞 전화하기</a>
            <a href="sms:${shop.tel}" class="cm2-btn-sms">💬 문자하기</a>
          </div>
        </div>
      `;
    });
    shopContainer.innerHTML = shopHtml;
  });
</script>
"""

region_desc_pool_1 = ["출장 마사지 및 홈타이 전문 안내.", "프라이빗 출장 마사지 서비스.", "맞춤형 홈타이 테라피 안내."]
region_desc_pool_2 = ["전 지역 평균 30분 내 신속 방문.", "자택 및 오피스텔로 찾아가는 1:1 홈타이 케어.", "어디서나 편안하게 즐기는 출장 마사지 힐링."]
region_desc_pool_3 = ["건식 6만원부터 시작하는 100% 후불제.", "심야 할증 없는 정찰제 출장 마사지.", "선입금 없는 투명한 후불제 홈타이 운영."]

dong_desc_pool_1 = ["출장 마사지 및 홈타이 맞춤 안내.", "방문 홈타이 서비스 실시간 안내.", "프라이빗 출장 마사지 힐링 케어."]
dong_desc_pool_2 = ["신속한 방문과 편안한 휴식을 보장하는 홈타이.", "자택·숙소 어디든 30분 내 찾아가는 출장 마사지.", "익숙한 공간에서 누리는 전문 홈타이 테라피."]
dong_desc_pool_3 = ["건식 6만원부터 시작하는 100% 후불제 출장마사지.", "심야 시간에도 추가 비용 없는 정찰제 홈타이.", "예약금 없이 안전하게 이용하는 후불제 서비스."]

region_template = Template(f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>$region_name 출장마사지·스웨디시 홈케어 예약 | 서울건마사랑</title>
<meta name="description" content="$region_desc">
<style>{common_style}</style></head><body>
<header class="cm2-hd"><div class="cm2-hd-inner"><a href="/" class="cm2-logo-text">서울건마사랑</a><a href="/" style="font-size:13px;color:#7a5c60;">🏠 홈으로</a></div></header>
<main>
  <nav class="cm2-bc"><div class="cm2-bc-inner"><a href="/">서울건마사랑</a> › <a href="/">서울</a> › $region_name</div></nav>
  
  <section class="cm2-sec">  
    <div class="cm2-sec-inner">    
      <div class="cm2-sec-hd">      
        <h1 class="cm2-page-h1">$region_name 출장마사지 및 홈타이 종합 안내</h1>      
        <p class="cm2-sec-sub">$region_name 전 지역 30분 내 신속 방문 — 세부 동네를 선택하거나 제휴 샵 연락처를 확인하세요</p>    
      </div>    
      
      <div style="background:#fff;border-left:3px solid #8a1f34;padding:22px;border-radius:0 8px 8px 0;margin-bottom:25px;box-shadow:0 2px 8px rgba(0,0,0,0.02);">
        <p style="font-size:15px;line-height:1.8;"><b>📍 $region_name 지역 특성 및 맞춤 방문 안내:</b> $intro</p>
        <p style="font-size:15px;line-height:1.8;margin-top:12px;">$region_name 어디든 자택, 오피스텔, 원룸, 숙소 등 고객님이 머무시는 편안한 공간으로 전문 관리사가 직접 찾아갑니다. 무거운 장비를 직접 들고 이동하거나 샵을 찾아 헤맬 필요 없이, 제휴 샵 연락처를 통해 $region_name 전역에서 프리미엄 힐링 케어를 받으실 수 있습니다.</p>
      </div>    
      
      <h3 style="font-size:17px;font-weight:800;margin-bottom:12px;color:var(--p);">$region_name 세부 동네 선택</h3>
      <div class="cm2-dong-grid" style="margin-bottom:35px;">
        $dong_cards_html
      </div>  

      <div class="cm2-sec-hd">
        <h2>$region_name 추천 제휴 샵 (5개소)</h2>
        <p class="cm2-sec-sub">새로고침할 때마다 제휴 업소 순서가 랜덤으로 변경되며, 바로 통화 및 문자가 가능합니다.</p>
      </div>
      <div id="random-shop-list" class="cm2-shop-grid" style="margin-bottom:35px;"></div>

      <div class="cm2-sec-hd"><h2>$region_name 방문 마사지, 이런 점이 궁금해요</h2></div>
      <div style="background:#fff;padding:22px;border-radius:10px;border:1px solid var(--bdr);margin-bottom:35px;">
        <p style="font-size:14px;line-height:1.8;color:var(--txt);">많은 고객님들께서 집이나 오피스텔로 관리사를 부르는 것에 대해 보안이나 위생, 준비 사항 등을 걱정하십니다. $region_name 홈타이 서비스는 철저한 신원 검증과 위생 교육을 이수한 전문 테라피스트가 최고급 아로마 오일과 매트를 직접 지참하여 방문하므로, 고객님께서는 별도의 준비물 없이 편안하게 누워 계시기만 하면 됩니다. 특히 외부 시선으로부터 완전히 자유로운 프라이빗한 공간에서 관리가 진행되므로 남녀노소 누구나 안심하고 이용하실 수 있습니다.</p>
      </div>

      <div class="cm2-sec-hd"><h2>$region_name 홈타이 이용 절차</h2></div>
      <div class="cm2-step-grid" style="margin-bottom:35px;">
        <div class="cm2-step-card">
          <strong>1단계. 제휴 샵 문의</strong>
          <p>고객님이 계신 $region_name 내 상세 위치와 원하시는 코스를 제휴 샵 번호로 문의해 주세요.</p>
        </div>
        <div class="cm2-step-card">
          <strong>2단계. 신속 이동 및 배정</strong>
          <p>예약 확정 즉시 $region_name 인근에 대기 중인 전담 관리사가 배정되어 신속하게 이동합니다.</p>
        </div>
        <div class="cm2-step-card">
          <strong>3단계. 프라이빗 케어</strong>
          <p>도착 후 관리사가 세팅 도구를 펼치고 고객님의 피로 부위에 맞춘 1:1 맞춤 케어를 시작합니다.</p>
        </div>
        <div class="cm2-step-card">
          <strong>4단계. 100% 후불 결제</strong>
          <p>모든 케어 서비스가 완벽하게 끝난 안전한 후불 결제 시스템으로 요금을 지불합니다.</p>
        </div>
      </div>

      <div class="cm2-sec-hd"><h2>$region_name에서 받을 수 있는 코스 안내</h2></div>
      <p class="cm2-sec-sub" style="margin-bottom:12px;">$region_name 전 지역 동일 적용 · 심야 할증 없음 · 100% 후불제</p>
      <table class="cm2-price-tbl" style="margin-bottom:35px;">
        <tr><th>코스 분류</th><th>세부 프로그램 설명</th><th>시간 및 이용 요금</th></tr>
        <tr><td style="font-weight:700;color:var(--p)">건식케어 (타이)</td><td>전통 타이 기법으로 뭉친 근육을 부드럽게 이완시키는 기본 프로그램</td><td>60분 6만원 / 90분 9만원 / 120분 11만원</td></tr>
        <tr><td style="font-weight:700;color:var(--p)">습식케어 (아로마)</td><td>천연 아로마 오일을 활용해 심신 안정과 혈액순환을 돕는 프로그램</td><td>60분 8만원 / 90분 10만원 / 120분 12만원</td></tr>
        <tr><td style="font-weight:700;color:var(--p)">오일케어 (감성힐링)</td><td>부드러운 터치와 깊은 이완을 선사하는 프리미엄 힐링 케어</td><td>60분 9만원 / 90분 11만원 / 120분 13만원</td></tr>
        <tr><td style="font-weight:700;color:var(--p)">VVIP 전신혼합</td><td>건식과 습식이 결합된 종합 토탈 바디 리프레시 프로그램</td><td>60분 10만원 / 90분 12만원 / 120분 14만원 / 150분 17만원</td></tr>
        <tr><td style="font-weight:700;color:var(--p)">한국인 스웨디시</td><td>한국인 전문 테라피스트의 섬세한 스웨디시 감성 테라피</td><td>60분 14만원 / 90분 18만원</td></tr>
      </table>

      <div class="cm2-sec-hd"><h2>$region_name 자주 묻는 질문 (FAQ)</h2></div>
      <div class="cm2-faq">
        <details open><summary>$region_name 모든 동네에 정말 다 방문이 가능한가요?</summary><p>네, $region_name 내 주거지, 오피스텔, 원룸, 숙소 등 차량 접근이 가능한 곳이라면 어디든 신속하게 방문합니다. 제휴 샵 연락처로 정확한 위치를 알려주시면 가장 가까운 관리사를 배정해 드립니다.</p></details>
        <details><summary>결제는 선불인가요, 후불인가요?</summary><p>저희 서울건마사랑 제휴 샵들은 고객님의 신뢰를 위해 100% 후불제로 운영하고 있습니다. 관리가 모두 끝난 후에 현금, 계좌이체, 카드 중 편하신 방법으로 결제하시면 됩니다.</p></details>
        <details><summary>늦은 새벽이나 주말에도 요금이 똑같나요?</summary><p>물론입니다. $region_name 전 지역에서 24시간 연중무휴로 운영되며, 심야 시간이나 주말이라고 해서 별도의 할증 요금을 부과하지 않습니다.</p></details>
      </div>

    </div>
  </section>
</main>
<footer class="cm2-ft"><div class="cm2-sec-inner"><p>© 2026 서울건마사랑. All rights reserved.</p></div></footer>
{shops_script}
</body></html>""")

dong_template = Template(f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>$dong_name 출장마사지·스웨디시 홈케어 예약 | 서울건마사랑</title>
<meta name="description" content="$dong_desc">
<style>{common_style}</style></head><body>
<header class="cm2-hd"><div class="cm2-hd-inner"><a href="/" class="cm2-logo-text">서울건마사랑</a><a href="/seoul/$key/" style="font-size:13px;color:#7a5c60;">📍 $region_name 목록</a></div></header>
<main>
  <nav class="cm2-bc"><div class="cm2-bc-inner"><a href="/">서울건마사랑</a> › <a href="/seoul/$key/">$region_name</a> › $dong_name</div></nav>
  
  <section class="cm2-sec">  
    <div class="cm2-sec-inner">    
      <div class="cm2-sec-hd">      
        <h1 class="cm2-page-h1">$dong_name 방문 마사지 및 홈타이 맞춤 안내</h1>      
        <p class="cm2-sec-sub">$dong_name 일대 30분 내 신속 방문 케어 — 프라이빗한 힐링 서비스를 만나보세요</p>    
      </div>    
      
      <div style="background:#fff;border-left:3px solid #8a1f34;padding:22px;border-radius:0 8px 8px 0;margin-bottom:25px;box-shadow:0 2px 8px rgba(0,0,0,0.02);">
        <p style="font-size:15px;line-height:1.8;"><b>📍 $dong_name 지역 맞춤 방문 케어 안내:</b> $dong_name 주변은 조용한 주거 단지와 오피스텔이 어우러져 있어, 외부로 멀리 나가지 않고 자택이나 편안한 숙소 안에서 마사지를 받고자 하시는 분들의 문의가 매우 많은 곳입니다.</p>
        <p style="font-size:15px;line-height:1.8;margin-top:12px;">교통망이 잘 연결되어 있어 제휴 샵을 통해 $dong_name 인근에 대기 중인 전문 관리사가 고객님의 프라이빗한 공간으로 신속하게 찾아갑니다. 늦은 야근 후 귀가하신 직장인 분들이나 집에서 편안하게 피로를 풀고 싶으신 분들께 최적의 만족을 드립니다.</p>
      </div>    

      <div class="cm2-sec-hd">
        <h2>$dong_name 추천 제휴 샵 (5개소)</h2>
        <p class="cm2-sec-sub">새로고침할 때마다 제휴 업소 순서가 랜덤으로 변경되며, 바로 통화 및 문자가 가능합니다.</p>
      </div>
      <div id="random-shop-list" class="cm2-shop-grid" style="margin-bottom:35px;"></div>

      <div class="cm2-sec-hd"><h2>$dong_name 방문 마사지, 이런 점이 궁금해요</h2></div>
      <div style="background:#fff;padding:22px;border-radius:10px;border:1px solid var(--bdr);margin-bottom:35px;">
        <p style="font-size:14px;line-height:1.8;color:var(--txt);">“집에 누군가를 부르는 게 처음이라 어색하지 않을까요?” $dong_name에서 처음 홈타이를 이용하시는 고객님들께서 종종 하시는 말씀입니다. 저희 서비스는 철저한 전문 소독과 위생 관리를 거친 최고급 매트와 타올, 아로마 용품을 직접 구비하여 방문하므로 고객님께서 따로 준비하실 것이 전혀 없습니다. $dong_name 내 자택, 오피스텔 등 익숙하고 편안한 본인의 공간에서 남의 시선 신경 쓸 필요 없이 온전히 휴식에만 집중하실 수 있습니다.</p>
      </div>

      <div class="cm2-sec-hd"><h2>$dong_name 홈타이 이용 절차</h2></div>
      <div class="cm2-step-grid" style="margin-bottom:35px;">
        <div class="cm2-step-card">
          <strong>1단계. 제휴 샵 문의</strong>
          <p>$dong_name 내 상세 주소와 원하시는 케어 코스를 제휴 샵 번호로 간편하게 접수해 주세요.</p>
        </div>
        <div class="cm2-step-card">
          <strong>2단계. 담당 관리사 배정</strong>
          <p>접수 즉시 $dong_name 인근에서 대기 중인 전문 관리사가 배정되어 신속하게 출발합니다.</p>
        </div>
        <div class="cm2-step-card">
          <strong>3단계. 1:1 맞춤 방문 케어</strong>
          <p>도착 후 세팅을 마치고 고객님의 신체 컨디션과 뭉친 근육 상태에 맞춘 집중 힐링 관리가 진행됩니다.</p>
        </div>
        <div class="cm2-step-card">
          <strong>4단계. 후불 결제 진행</strong>
          <p>모든 케어 프로그램이 완전히 끝난 후 만족스러우실 때 요금을 지불하는 100% 후불제 시스템입니다.</p>
        </div>
      </div>

      <div class="cm2-sec-hd"><h2>$dong_name에서 받을 수 있는 코스 안내</h2></div>
      <p class="cm2-sec-sub" style="margin-bottom:12px;">$dong_name 전 지역 동일 요금 · 심야 할증 없음 · 100% 후불 결제</p>
      <table class="cm2-price-tbl" style="margin-bottom:35px;">
        <tr><th>코스 분류</th><th>세부 프로그램 설명</th><th>시간 및 이용 요금</th></tr>
        <tr><td style="font-weight:700;color:var(--p)">건식케어 (타이)</td><td>전통 타이 기법을 바탕으로 $dong_name 주민들의 뭉친 등·허리 근육을 시원하게 풀어주는 코스</td><td>60분 6만원 / 90분 9만원 / 120분 11만원</td></tr>
        <tr><td style="font-weight:700;color:var(--p)">습식케어 (아로마)</td><td>순환을 돕는 고급 아로마 오일을 사용하여 부드럽고 깊은 이완을 선사하는 코스</td><td>60분 8만원 / 90분 10만원 / 120분 12만원</td></tr>
        <tr><td style="font-weight:700;color:var(--p)">오일케어 (감성힐링)</td><td>지친 일상에 깊은 휴식과 힐링 에너지를 채워주는 프리미엄 터치 프로그램</td><td>60분 9만원 / 90분 11만원 / 120분 13만원</td></tr>
        <tr><td style="font-weight:700;color:var(--p)">VVIP 전신혼합</td><td>건식과 아로마, 스페셜 케어가 모두 포함된 최고급 토탈 릴렉싱 코스</td><td>60분 10만원 / 90분 12만원 / 120분 14만원 / 150분 17만원</td></tr>
        <tr><td style="font-weight:700;color:var(--p)">한국인 스웨디시</td><td>한국인 전문 관리사만의 섬세하고 부드러운 감성 스웨디시 케어</td><td>60분 14만원 / 90분 18만원</td></tr>
      </table>

      <div class="cm2-sec-hd"><h2>$dong_name 자주 묻는 질문 (FAQ)</h2></div>
      <div class="cm2-faq">
        <details open><summary>$dong_name 오피스텔이나 원룸인데 방문이 되나요?</summary><p>네, $dong_name 내 모든 주거 형태(아파트, 오피s텔, 빌라, 원룸) 및 숙소에서 편리하게 이용하실 수 있습니다. 차량 주차가 가능하고 진입이 가능한 곳이라면 어디든 찾아갑니다.</p></details>
        <details><summary>결제는 언제 어떻게 하나요?</summary><p>선입금이나 예약금 요구 없이 100% 후불제로 안전하게 운영됩니다. $dong_name에서의 관리가 모두 끝난 후 현금, 카드, 계좌이체 중 편하신 방법으로 결제해 주세요.</p></details>
        <details><summary>늦은 밤이나 새벽 시간에도 추가 비용이 없나요?</summary><p>없습니다! $dong_name 홈타이 서비스는 24시간 연중무휴로 운영되며, 밤늦은 시간이나 새벽에 이용하시더라도 평일 낮과 동일한 정직한 요금으로 이용하실 수 있습니다.</p></details>
      </div>

    </div>
  </section>
</main>
<footer class="cm2-ft"><div class="cm2-sec-inner"><p>© 2026 서울건마사랑. All rights reserved.</p></div></footer>
{shops_script}
</body></html>""")

# 생성 실행 루프 및 robots.txt, sitemap.xml 자동 생성
urls = [f"{BASE_URL}/"]
for key, data in regions.items():
    dir_path = f"seoul/{key}"
    os.makedirs(dir_path, exist_ok=True)
    urls.append(f"{BASE_URL}/seoul/{key}/")
    
    dong_cards_html = ""
    for dong in data["dongs"]:
        dong_name = dong["name"]
        dong_slug = dong["slug"]
        
        dong_cards_html += f'<a href="{dong_slug}/" class="cm2-dong-card"><strong>{dong_name}</strong><span>맞춤 케어</span></a>\n'
        urls.append(f"{BASE_URL}/seoul/{key}/{dong_slug}/")
        
        dong_dir_path = f"seoul/{key}/{dong_slug}"
        os.makedirs(dong_dir_path, exist_ok=True)
        
        dong_desc = f"{data['name']} {dong_name} {random.choice(dong_desc_pool_1)} {random.choice(dong_desc_pool_2)} {random.choice(dong_desc_pool_3)}"
        
        final_dong_html = dong_template.safe_substitute(
            key=key,
            region_name=data["name"],
            dong_name=dong_name,
            dong_slug=dong_slug,
            dong_desc=dong_desc
        )
        
        with open(f"{dong_dir_path}/index.html", "w", encoding="utf-8") as f_dong:
            f_dong.write(final_dong_html)
        
    region_desc = f"{data['name']} {random.choice(region_desc_pool_1)} {random.choice(region_desc_pool_2)} {random.choice(region_desc_pool_3)}"
    
    final_region_html = region_template.safe_substitute(
        key=key,
        region_name=data["name"],
        intro=data["intro"],
        dong_cards_html=dong_cards_html,
        region_desc=region_desc
    )
    
    with open(f"{dir_path}/index.html", "w", encoding="utf-8") as f_region:
        f_region.write(final_region_html)

# 1. robots.txt 생성
robots_txt = """User-agent: *
Allow: /

Sitemap: https://seoulm-gunmalove02.netlify.app/sitemap.xml
"""
with open("robots.txt", "w", encoding="utf-8") as f_robots:
    f_robots.write(robots_txt)

# 2. sitemap.xml 생성
sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url in urls:
    sitemap_xml += f"  <url>\n    <loc>{url}</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n"
sitemap_xml += '</urlset>'

with open("sitemap.xml", "w", encoding="utf-8") as f_sitemap:
    f_sitemap.write(sitemap_xml)
        
print("✨ 구와 동 페이지 모두 전화/문자 버튼 세팅 완료! 추가로 robots.txt와 sitemap.xml까지 완벽하게 자동 생성되었습니다!")