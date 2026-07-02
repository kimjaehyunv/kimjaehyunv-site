# kimjaehyunv-site — 사진 운영 매뉴얼

JAEHYUN KIM 포트폴리오 사이트의 사진을 관리하는 방법입니다.

**운영자가 직접 수정하는 파일**

- `images/work/slides.txt` — WORK 페이지
- `images/jaehyun/slides.txt` — JAEHYUN 페이지
- `images/work/originals/` — WORK **원본 JPG** (여기에만 넣기)
- `images/jaehyun/originals/` — JAEHYUN **원본 JPG** (여기에만 넣기)

JavaScript, CSS, HTML, `gallery.json`, 웹용 JPG, `.webp` 파일은 **수정하지 마세요.**  
Update Gallery 실행 시 `originals/` 원본 → 웹용 JPG + WebP + gallery.json 이 자동 생성됩니다.

> **원본 JPG는 `originals/` 폴더에만 넣으세요.** Update Gallery를 여러 번 실행해도 `originals/` 파일은 절대 변경되지 않습니다.

---

## slides.txt 기본 규칙

| 규칙 | 설명 |
|------|------|
| 한 줄 = 슬라이드 한 장 | 위에서 아래 순서 = 사이트에서 보이는 순서 |
| `01.jpg` | 사진 한 장짜리 슬라이드 |
| `02a.jpg + 02b.jpg` | + 로 이어서 한 슬라이드에 여러 장 |
| `[키워드] ...` | 특수 레이아웃 (아래 표 참고) |
| `# ...` | 메모 (무시됨) |

**순서는 slides.txt 줄 순서가 기준입니다.** 파일 이름 번호와 달라도 됩니다.

---

## 02a / 02b 사용법

### 한 슬라이드에 두 장 (JAEHYUN pair)

```
[pair] 02a.jpg + 02b.jpg
03.jpg
```

### 각각 별도 슬라이드

```
02a.jpg
02b.jpg
03.jpg
```

### WORK에서 여러 장 묶기

```
[spread] 06.jpg + 07.jpg + 08.jpg + 09.jpg
[spread-lower] 10.jpg + 11.jpg
```

---

## 키워드 목록

### WORK (`images/work/slides.txt`)

| 키워드 | 용도 |
|--------|------|
| `[spread]` | 4장 상단 그리드 |
| `[spread-lower]` | 2장 하단 그리드 (바로 위 spread 와 열 정렬) |
| `[spread-quad]` | 4장 quad 그리드 |

### JAEHYUN (`images/jaehyun/slides.txt`)

| 키워드 | 용도 |
|--------|------|
| `[opening]` | 첫 장 강조 |
| `[closing]` | 마지막 장 강조 |
| `[reduced]` | 작게 표시 |
| `[reduced-forty]` | 더 작게 표시 |
| `[small]` | 작은 크기 |
| `[lower-left]` | 왼쪽 아래 배치 |
| `[contact]` | 4장 contact sheet |
| `[pair]` | 2장 비대칭 pair |

---

## 사진 추가

1. 사진 파일을 준비합니다 (`32.jpg` 또는 `15a.jpg`, `15b.jpg` 등).
2. `images/work/originals/` 또는 `images/jaehyun/originals/` 폴더에 **원본 JPG**를 넣습니다.
3. 해당 `slides.txt` 에 **원하는 위치에 한 줄**을 추가합니다.
   - 한 장: `32.jpg`
   - 두 장 한 슬라이드: `[pair] 32a.jpg + 32b.jpg`
4. **Update Gallery.command** 를 더블클릭합니다.
   - 원본 JPG → 웹용 JPG 생성
   - WebP 자동 생성
   - gallery.json 자동 생성
5. 변경 사항을 GitHub에 push 하면 사이트에 반영됩니다.

> **원본은 `originals/`에만 넣으세요.** WebP와 웹용 JPG는 자동 생성됩니다.

---

## 사진 삭제

1. `slides.txt` 에서 해당 줄을 **삭제**합니다.
2. `originals/` 에서 **원본 JPG**를 삭제합니다.
3. (선택) 웹용 JPG와 WebP도 삭제
4. **Update Gallery.command** 를 더블클릭합니다.
5. GitHub에 push 합니다.

---

## 순서 변경

1. `slides.txt` 에서 줄을 **잘라내기 → 붙여넣기**로 이동합니다.
2. 파일 이름을 바꿀 필요는 없습니다.
3. **Update Gallery.command** 를 더블클릭합니다.
4. GitHub에 push 합니다.

---

## Update Gallery.command 실행 방법

1. Finder에서 프로젝트 폴더(`kimjaehyunv-site`)를 엽니다.
2. **Update Gallery.command** 파일을 **더블클릭**합니다.
3. 터미널 창이 열리며 아래 작업이 자동으로 실행됩니다.
   - `originals/` 원본 JPG 읽기 (원본은 수정하지 않음)
   - 웹용 JPG 생성 (JPEG quality 88)
   - WebP 자동 생성 (quality 86)
   - gallery.json 자동 생성
4. "Done" 메시지가 나오면 Enter 를 눌러 창을 닫습니다.

**처음 실행 시 Mac이 차단할 수 있습니다.**

- `시스템 설정 → 개인정보 보호 및 보안` 에서 실행 허용
- 또는 파일을 우클릭 → **열기** → **열기** 확인

**터미널에서 실행하려면:**

```bash
cd /path/to/kimjaehyunv-site
python3 scripts/build-gallery.py
```

---

## 자동 생성 파일 (수정 금지)

| 파일 | 설명 |
|------|------|
| `images/work/gallery.json` | WORK 슬라이드 데이터 (자동 생성) |
| `images/jaehyun/gallery.json` | JAEHYUN 슬라이드 데이터 (자동 생성) |
| `images/*/*.jpg` (originals 제외) | 웹용 최적화 JPG (originals에서 자동 생성) |
| `images/*/*.webp` | WebP 최적화 파일 (자동 생성) |

---

## INFO 페이지

INFO 프로필 사진(`images/info/02.jpg`)은 `slides.txt` 와 별개입니다. 자주 바꾸지 않는다면 `index.html` 의 img 경로를 직접 수정하거나, 나중에 동일 방식으로 확장할 수 있습니다.

---

## 프로젝트 구조

```
kimjaehyunv-site/
├── Update Gallery.command    ← 더블클릭으로 gallery 갱신
├── README.md                 ← 이 파일
├── index.html
├── css/style.css
├── js/
│   ├── main.js
│   ├── slides.js
│   ├── work-slides.js
│   └── mobile.js
├── images/
│   ├── work/
│   │   ├── slides.txt        ← WORK 운영자 편집
│   │   ├── originals/        ← WORK 원본 JPG (운영자가 여기에만 추가)
│   │   ├── gallery.json      ← 자동 생성
│   │   ├── *.jpg             ← 웹용 JPG (자동 생성)
│   │   └── *.webp            ← 자동 생성
│   └── jaehyun/
│       ├── slides.txt        ← JAEHYUN 운영자 편집
│       ├── originals/        ← JAEHYUN 원본 JPG (운영자가 여기에만 추가)
│       ├── gallery.json      ← 자동 생성
│       ├── *.jpg             ← 웹용 JPG (자동 생성)
│       └── *.webp            ← 자동 생성
└── scripts/
    ├── build-gallery.py      ← JPG 최적화 + WebP + gallery.json 생성
    └── optimize-images.py    ← 이미지 최적화 로직
```
