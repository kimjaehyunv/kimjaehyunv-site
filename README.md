# kimjaehyunv-site — 사진 운영 매뉴얼

JAEHYUN KIM 포트폴리오 사이트의 사진을 관리하는 방법입니다.  
**Cursor 없이** Mac에서 사진만 관리하고 사이트를 업데이트할 수 있습니다.

---

## 한 줄 요약

1. **추가:** `originals/`에 원본 JPG 넣기 + `slides.txt`에 한 줄 추가  
2. **삭제:** `slides.txt`에서 한 줄만 삭제  
3. **순서 변경:** `slides.txt`에서 줄 이동  
4. **`Update Gallery.command` 더블클릭** → 끝

---

## 처음 한 번만 설정

### 1. Mac에서 Update Gallery.command 실행 허용

- **시스템 설정 → 개인정보 보호 및 보안** 에서 실행 허용  
- 또는 파일 **우클릭 → 열기 → 열기**

### 2. Python Pillow 설치

```bash
python3 -m pip install Pillow
```

### 3. GitHub 로그인

```bash
gh auth login
```

또는 **GitHub Desktop** 으로 로그인.

---

## 운영자가 직접 수정하는 것

| 수정함 | 설명 |
|--------|------|
| `images/work/originals/` | WORK 원본 JPG **추가** |
| `images/jaehyun/originals/` | JAEHYUN 원본 JPG **추가** |
| `images/work/slides.txt` | WORK 슬라이드 순서·목록 |
| `images/jaehyun/slides.txt` | JAEHYUN 슬라이드 순서·목록 |

| 직접 수정/삭제하지 않음 | 설명 |
|------------------------|------|
| `gallery.json` | 자동 생성 |
| 웹용 JPG, WebP | 자동 생성·삭제 |
| `originals/` 파일 삭제 | **slides.txt에서 줄만 삭제하면 자동 정리** |
| JS, CSS, HTML | 개발자 전용 |

> **참조 중인 원본은 절대 수정되지 않습니다.**  
> Update Gallery는 `originals/` 파일을 **읽기만** 하고, 내용을 바꾸지 않습니다.  
> `originals/` 는 **이 Mac에만** 두고 GitHub·Cloudflare에는 올라가지 않습니다 (웹용 JPG/WebP만 배포됩니다).

---

## Update Gallery.command — 전체 자동화

더블클릭 한 번으로 아래가 **순서대로 모두** 실행됩니다.

| 단계 | 작업 |
|------|------|
| 1/4 | `slides.txt`에 **없는** 파일 자동 삭제 (originals + 웹 JPG + WebP) |
| 2/4 | `originals/` → 웹용 JPG + WebP 생성 (**새/변경분만**) |
| 3/4 | `gallery.json` 생성 |
| 4/4 | `git add` → `git commit` → `git push origin main` |

성공 시 **Commit hash** 와 **GitHub push successful** 이 표시됩니다.  
1~2분 후 [kimjaehyunv.com](https://kimjaehyunv.com) 에 반영됩니다.

---

## 사진 추가하기

**예: JAEHYUN에 33.jpg 추가**

1. `33.jpg` 원본을 `images/jaehyun/originals/` 에 복사합니다.
2. `images/jaehyun/slides.txt` 에 한 줄 추가:
   ```
   33.jpg
   ```
3. **`Update Gallery.command` 더블클릭**

**두 장 한 슬라이드 (pair):**

```
[pair] 33a.jpg + 33b.jpg
```

→ `originals/`에 `33a.jpg`, `33b.jpg` 넣고 slides.txt에 위 한 줄 추가.

---

## 사진 삭제하기

**예: 33.jpg 삭제**

1. `images/jaehyun/slides.txt` 에서 `33.jpg` **줄만 삭제**합니다.
2. **`Update Gallery.command` 더블클릭**

자동으로 삭제되는 파일:

- `images/jaehyun/originals/33.jpg`
- `images/jaehyun/33.jpg` (웹용)
- `images/jaehyun/33.webp`

`gallery.json`도 slides.txt 기준으로 다시 생성됩니다.

> **originals/ 폴더에서 직접 삭제할 필요 없습니다.**

---

## 순서 변경하기

1. `slides.txt` 에서 줄을 **잘라내기 → 붙여넣기**로 이동합니다.
2. 파일 이름 변경은 **불필요**합니다.
3. **`Update Gallery.command` 더블클릭**

---

## slides.txt 기본 규칙

| 규칙 | 설명 |
|------|------|
| 한 줄 = 슬라이드 한 장 | 위 → 아래 = 사이트 순서 |
| `01.jpg` | 사진 한 장 |
| `02a.jpg + 02b.jpg` | + 로 여러 장 한 슬라이드 |
| `[키워드] ...` | 특수 레이아웃 |
| `# ...` | 메모 (무시됨) |

### 키워드 (WORK)

| 키워드 | 용도 |
|--------|------|
| `[spread]` | 4장 상단 그리드 |
| `[spread-lower]` | 2장 하단 그리드 |
| `[spread-quad]` | 4장 quad 그리드 |

### 키워드 (JAEHYUN)

| 키워드 | 용도 |
|--------|------|
| `[opening]` / `[closing]` | 첫·마지막 장 강조 |
| `[reduced]` / `[reduced-forty]` / `[small]` | 크기 조절 |
| `[lower-left]` | 왼쪽 아래 배치 |
| `[contact]` | 4장 contact sheet |
| `[pair]` | 2장 비대칭 pair |

---

## 문제 해결

| 증상 | 해결 |
|------|------|
| Gallery build failed | `python3 -m pip install Pillow` |
| git push failed | `gh auth login` 또는 GitHub Desktop 로그인 |
| 사진이 안 보임 | slides.txt에 파일명 있는지, originals/에 JPG 있는지 확인 |

---

## 폴더 구조

```
kimjaehyunv-site/
├── Update Gallery.command    ← ★ 더블클릭만 하면 전체 완료
├── images/
│   ├── work/
│   │   ├── originals/        ← 원본 JPG 추가 (삭제는 slides.txt에서)
│   │   ├── slides.txt        ← ★ 순서·목록 관리
│   │   ├── gallery.json      ← 자동
│   │   ├── *.jpg / *.webp    ← 자동
│   └── jaehyun/
│       ├── originals/
│       ├── slides.txt
│       └── ...
└── scripts/
    ├── build-gallery.py
    ├── optimize-images.py
    └── publish-gallery.sh
```
