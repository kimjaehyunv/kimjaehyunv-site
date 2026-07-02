# kimjaehyunv-site — 사진 운영 매뉴얼

JAEHYUN KIM 포트폴리오 사이트의 사진을 관리하는 방법입니다.  
**Cursor 없이** Mac에서 사진만 관리하고 사이트를 업데이트할 수 있습니다.

---

## 한 줄 요약

1. `originals/` 폴더에 **원본 JPG** 넣기  
2. `slides.txt` 수정 (순서·목록)  
3. **`Update Gallery.command` 더블클릭**  
4. 끝 — 사이트에 자동 반영됩니다

---

## 처음 한 번만 설정

### 1. Mac에서 Update Gallery.command 실행 허용

처음 더블클릭 시 Mac이 차단할 수 있습니다.

- **시스템 설정 → 개인정보 보호 및 보안** 에서 실행 허용  
- 또는 파일 **우클릭 → 열기 → 열기** 로 한 번 실행

### 2. Python Pillow 설치 (이미지 처리용)

터미널에서 한 번 실행:

```bash
python3 -m pip install Pillow
```

### 3. GitHub 로그인 (사이트 배포용)

터미널에서 한 번 실행:

```bash
gh auth login
```

또는 **GitHub Desktop** 앱으로 로그인해 두어도 됩니다.

---

## 운영자가 직접 수정하는 것

| 수정함 | 설명 |
|--------|------|
| `images/work/originals/` | WORK 원본 JPG |
| `images/jaehyun/originals/` | JAEHYUN 원본 JPG |
| `images/work/slides.txt` | WORK 슬라이드 순서·구성 |
| `images/jaehyun/slides.txt` | JAEHYUN 슬라이드 순서·구성 |

| 수정하지 않음 | 설명 |
|---------------|------|
| `gallery.json` | 자동 생성 |
| 웹용 JPG (`originals/` 밖) | 자동 생성 |
| `.webp` | 자동 생성 |
| JS, CSS, HTML | 개발자 전용 |

> **원본 JPG는 `originals/` 폴더에만 넣으세요.**  
> Update Gallery를 여러 번 실행해도 `originals/` 파일은 **절대 변경되지 않습니다.**

---

## Update Gallery.command — 전체 자동화

더블클릭 한 번으로 아래가 **순서대로 모두** 실행됩니다.

| 단계 | 작업 |
|------|------|
| 1 | `originals/` 원본 JPG 읽기 (원본 수정 없음) |
| 2 | 웹용 JPG 생성 (JPEG quality 88, **새/변경된 사진만**) |
| 3 | WebP 생성 (quality 86, **새/변경된 사진만**) |
| 4 | `gallery.json` 생성 |
| 5 | `git add` → `git commit` → `git push origin main` |

성공 시 터미널에 **Commit hash** 와 **GitHub push successful** 이 표시됩니다.  
1~2분 후 [kimjaehyunv.com](https://kimjaehyunv.com) 에 반영됩니다.

변경 사항이 없으면 `"No gallery changes to commit"` 이 표시되고 push는 건너뜁니다.

---

## 사진 추가하기

**예: JAEHYUN에 33.jpg 추가**

1. 원본 파일 `33.jpg` 를 준비합니다.
2. Finder에서 `images/jaehyun/originals/` 폴더에 `33.jpg` 를 **복사**합니다.
3. 텍스트 편집기로 `images/jaehyun/slides.txt` 를 엽니다.
4. 원하는 위치에 한 줄 추가:
   ```
   33.jpg
   ```
5. 저장합니다.
6. **`Update Gallery.command` 더블클릭**합니다.
7. 터미널에 `GitHub push successful` 이 나오면 완료입니다.

**두 장을 한 슬라이드에 넣을 때 (pair):**

```
[pair] 33a.jpg + 33b.jpg
```

→ `originals/` 에 `33a.jpg`, `33b.jpg` 두 파일을 넣고, slides.txt에 위 한 줄을 추가합니다.

---

## 사진 삭제하기

**예: 33.jpg 삭제**

1. `images/jaehyun/slides.txt` 에서 `33.jpg` 줄을 **삭제**합니다.
2. `images/jaehyun/originals/33.jpg` 파일을 **삭제**합니다.
3. (선택) `images/jaehyun/33.jpg`, `33.webp` 도 삭제 — 없어도 다음 실행 시 정리됩니다.
4. **`Update Gallery.command` 더블클릭**합니다.

---

## 순서 변경하기

**예: 33.jpg를 10번째로 보이게**

1. `images/jaehyun/slides.txt` 를 엽니다.
2. `33.jpg` 줄을 **잘라내기(Cmd+X)** → 원하는 위치에 **붙여넣기(Cmd+V)** 합니다.
3. 파일 이름을 바꿀 필요는 **없습니다**.
4. **`Update Gallery.command` 더블클릭**합니다.

---

## slides.txt 기본 규칙

| 규칙 | 설명 |
|------|------|
| 한 줄 = 슬라이드 한 장 | 위 → 아래 = 사이트에서 보이는 순서 |
| `01.jpg` | 사진 한 장 |
| `02a.jpg + 02b.jpg` | + 로 여러 장을 한 슬라이드에 |
| `[키워드] ...` | 특수 레이아웃 |
| `# ...` | 메모 (무시됨) |

### 02a / 02b 사용법

**한 슬라이드에 두 장:**
```
[pair] 02a.jpg + 02b.jpg
```

**각각 별도 슬라이드:**
```
02a.jpg
02b.jpg
```

---

## 키워드 목록

### WORK (`images/work/slides.txt`)

| 키워드 | 용도 |
|--------|------|
| `[spread]` | 4장 상단 그리드 |
| `[spread-lower]` | 2장 하단 그리드 |
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

## 문제 해결

### Gallery build failed

- `python3 -m pip install Pillow` 실행 후 다시 시도

### git push failed

터미널에 원인이 출력됩니다. 흔한 경우:

| 원인 | 해결 |
|------|------|
| GitHub 로그인 만료 | `gh auth login` 또는 GitHub Desktop 로그인 |
| 인터넷 연결 | Wi-Fi 확인 후 다시 실행 |
| 권한 없음 | 저장소 접근 권한 확인 |

### 사진이 사이트에 안 보임

- `slides.txt` 에 파일명이 있는지 확인
- `originals/` 에 같은 이름의 JPG가 있는지 확인
- Update Gallery 실행 후 push 성공 메시지 확인

---

## 폴더 구조

```
kimjaehyunv-site/
├── Update Gallery.command    ← ★ 더블클릭만 하면 전체 완료
├── README.md
├── images/
│   ├── work/
│   │   ├── originals/        ← WORK 원본 JPG (여기에만 추가)
│   │   ├── slides.txt        ← WORK 순서·구성
│   │   ├── gallery.json      ← 자동 생성
│   │   ├── *.jpg             ← 웹용 JPG (자동 생성)
│   │   └── *.webp            ← 자동 생성
│   └── jaehyun/
│       ├── originals/        ← JAEHYUN 원본 JPG (여기에만 추가)
│       ├── slides.txt
│       ├── gallery.json
│       ├── *.jpg
│       └── *.webp
└── scripts/
    ├── build-gallery.py
    ├── optimize-images.py
    └── publish-gallery.sh
```

---

## INFO 페이지

INFO 프로필 사진(`images/info/02.jpg`)은 slides.txt 와 별개입니다.  
변경이 필요하면 `images/info/originals/` 에 원본을 넣고 Update Gallery를 실행하세요.
