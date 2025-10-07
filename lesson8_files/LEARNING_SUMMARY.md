# Lesson 8 学習サマリー

## 日付
2025年10月6日〜7日

## レッスンタイトル
Figmaデザインモックアップから実際のウェブアプリケーションを開発し、Vercelにデプロイする

---

## 学んだこと

### 1. レッスンの全体像

このレッスンでは、**デザイン画像から実際に動くウェブアプリケーションを作る**という、従来は数日〜数週間かかっていた作業を、Claude Codeを使って数分〜数時間で完成させる方法を学びました。

**2段階アプローチ：**
1. **第1段階**: ダミーデータで見た目を作る（完了）
2. **第2段階**: 本物のデータに置き換える（次回）

---

### 2. 使用技術とツール

#### Next.js
- **何か**: Reactを使いやすくしたフレームワーク
- **なぜ使う**: モダンなダッシュボードを作るのに最適
- **特徴**:
  - フォルダ構造＝ページ構造
  - ホットリロード（コード変更が即反映）
  - TypeScript対応

#### MCP (Model Context Protocol) サーバー
- **何か**: Claude Codeが他のツールと連携するための「通訳」
- **今回使ったMCPサーバー**:
  - **Playwright MCP Server**: ブラウザを自動操作してスクリーンショット撮影

#### Playwright
- **何か**: ブラウザ自動化ツール
- **できること**:
  - Webページを自動で開く
  - スクリーンショットを撮る
  - UIテストを自動化

#### Recharts
- **何か**: React用のグラフライブラリ
- **できること**: 折れ線グラフ、エリアチャート、棒グラフなど

---

### 3. 実施した手順

#### ステップ1: プロジェクトセットアップ
```bash
# Next.jsプロジェクト作成
npx create-next-app@latest my-app --typescript --tailwind --eslint

# グラフライブラリをインストール
npm install recharts
```

**場所**: `lesson8_files/my-app/`

---

#### ステップ2: MCP サーバー設定

**Playwright MCP Serverを追加：**
```bash
claude mcp add-json playwright '{"command":"npx","args":["-y","@executeautomation/playwright-mcp-server"]}'
```

**確認：**
```bash
claude mcp list
# → playwright: ✓ Connected
```

**重要ポイント**:
- MCPサーバーは、Claude Codeが外部ツール（Figma、Playwrightなど）と連携するための仕組み
- 設定ファイルは `~/.claude/` に保存される

---

#### ステップ3: デザイン参考画像の取得

**当初の計画**: Figma MCP Serverを使う
**問題**: Figma Dev Modeは有料プラン必須（月額$12〜）

**代替案（採用）**: 完成版リポジトリを起動してスクリーンショット

```bash
# 完成版をクローン
git clone https://github.com/https-deeplearning-ai/FRED-dashboard.git /tmp/FRED-dashboard

# 起動
cd /tmp/FRED-dashboard
npm install
npm run dev

# ブラウザで http://localhost:3000 を開いてスクリーンショット撮影
```

**学び**:
- 有料ツールがなくても、工夫次第で同じ学習効果が得られる
- スクリーンショットでも十分、デザインからコード生成できる

---

#### ステップ4: ダッシュボードのコード作成

**ファイル**: `app/page.tsx`

**構成**:
1. **サイドバー**:
   - FRED Indicators タイトル
   - ナビゲーションメニュー（Key Indicators、Inflation、Employment等）

2. **メインエリア**:
   - タイトル: "Economic Indicators Dashboard"
   - 4つのグラフカード（2×2グリッド）:
     - Consumer Price Index (CPI) - 青い折れ線グラフ
     - Unemployment Rate - 緑のエリアチャート
     - 10-Year Treasury Yield - 紫の折れ線グラフ
     - 3-Month Treasury Yield - オレンジの折れ線グラフ

**ダミーデータ例**:
```typescript
const cpiData = [
  { date: 'Dec 22', value: 296 },
  { date: 'Mar 23', value: 301 },
  // ...
];
```

**技術的なポイント**:
- `'use client'`: Reactのクライアントコンポーネント（インタラクティブな機能用）
- `Recharts`: LineChart, AreaChart を使用
- `Tailwind CSS`: `className` でスタイリング

---

#### ステップ5: Playwrightで自動確認

**目的**: デザインと実装が一致しているか自動確認

**手順**:
```bash
# Playwrightをインストール
npm install -D playwright
npx playwright install chromium

# スクリーンショット撮影スクリプト作成（screenshot.js）
node screenshot.js
```

**結果**: `dashboard-screenshot.png` が生成される

**スクリプトの内容**:
```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1920, height: 1080 });
  await page.goto('http://localhost:3000');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'dashboard-screenshot.png', fullPage: true });
  await browser.close();
})();
```

**学び**:
- 手動でスクリーンショットを撮るのではなく、自動化できる
- 継続的にデザインと実装の一致を確認できる（CI/CDに組み込める）

---

### 4. 重要な概念

#### なぜ2段階（ダミー → 本物）なのか？

**従来のやり方**:
```
デザイン + API + 見た目を全部同時に実装
→ どこで間違えたかわからない！
```

**Claude Code方式**:
```
第1段階: 見た目だけ作る（ダミーデータ）
→ デザインが正しいか確認

第2段階: データだけ本物に変える
→ API連携が正しいか確認

→ 問題を切り分けられる！
```

---

#### Next.jsを学ばなくてもいいのか？

**短期的**: このレッスンでは不要
**長期的**: 基礎は学んだ方がいい

**理由**:
1. より的確な指示が出せる
2. 生成されたコードが理解できる
3. エラーに対処できる

**推奨学習法**:
```
古い: 本を読む → チュートリアル → 実践
新しい: まず作る（Claude Code） → コードを読む → 少しずつ学ぶ
```

---

### 5. トラブルシューティング

#### Figma MCP Serverが有料だった
**解決策**: 完成版リポジトリからスクリーンショットを取得

#### MCPサーバーが認識されない
**原因**: 設定ファイルの場所が違った
**解決策**: `claude mcp add-json` コマンドを使用

---

### 6. プロジェクト構成

```
lesson8_files/
└── my-app/
    ├── app/
    │   ├── page.tsx              # メインダッシュボード（177行）
    │   ├── layout.tsx            # 全体レイアウト
    │   └── globals.css           # グローバルスタイル
    ├── public/                   # 静的ファイル
    ├── screenshot.js             # Playwrightスクリプト
    ├── dashboard-screenshot.png  # 自動撮影したスクリーンショット
    ├── package.json              # 依存関係
    └── tsconfig.json             # TypeScript設定
```

**インストールしたパッケージ**:
- `recharts`: グラフライブラリ
- `playwright`: ブラウザ自動化

---

### 7. FRED API連携の実装（10月7日完了）

#### ステップ1: APIキー取得
1. https://fred.stlouisfed.org/docs/api/api_key.html でアカウント作成
2. APIキーを取得: `b5cf166e62de7b5801024e71bac57823`
3. **セキュリティ**: APIキーは `.env.local` に保存（Gitにコミットしない）

#### ステップ2: 環境変数設定
```bash
# .env.local ファイル作成
NEXT_PUBLIC_FRED_API_KEY=b5cf166e62de7b5801024e71bac57823
```

**重要ポイント**:
- `.gitignore` に `.env.local` が含まれていることを確認
- APIキーを公開リポジトリにプッシュしないこと

#### ステップ3: CORS問題との遭遇

**問題**: ブラウザから直接FRED APIを呼ぶとCORSエラー
```
Access to fetch at 'https://api.stlouisfed.org/...' has been blocked by CORS policy
```

**原因**: FRED APIはブラウザからの直接アクセスを許可していない

**解決策**: Next.js API Route（サーバーサイドプロキシ）を作成

#### ステップ4: API Routeの実装

**ファイル**: `app/api/fred/route.ts`

```typescript
import { NextRequest, NextResponse } from 'next/server';

const FRED_API_KEY = process.env.NEXT_PUBLIC_FRED_API_KEY;
const FRED_API_BASE = 'https://api.stlouisfed.org/fred/series/observations';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const seriesId = searchParams.get('series_id');
  const limit = searchParams.get('limit') || '100';

  if (!seriesId) {
    return NextResponse.json({ error: 'series_id is required' }, { status: 400 });
  }

  try {
    const url = `${FRED_API_BASE}?series_id=${seriesId}&api_key=${FRED_API_KEY}&file_type=json&limit=${limit}&sort_order=desc`;
    const response = await fetch(url);

    if (!response.ok) throw new Error(`FRED API error: ${response.status}`);

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error(`Error fetching FRED data for ${seriesId}:`, error);
    return NextResponse.json({ error: 'Failed to fetch FRED data' }, { status: 500 });
  }
}
```

**仕組み**:
```
[ブラウザ] → [Next.js API Route] → [FRED API]
    ↑             サーバーサイド         ↓
    └──────────── データ返却 ←──────────┘
```

#### ステップ5: データ取得ユーティリティ作成

**ファイル**: `lib/fred.ts`

```typescript
export interface FredDataPoint {
  date: string;
  value: number;
}

interface FredObservation {
  date: string;
  value: string;
}

export async function fetchFredData(
  seriesId: string,
  limit: number = 100
): Promise<FredDataPoint[]> {
  try {
    const url = `/api/fred?series_id=${seriesId}&limit=${limit}`;
    const response = await fetch(url);

    if (!response.ok) throw new Error(`API error: ${response.status}`);

    const data = await response.json();
    const observations: FredObservation[] = data.observations || [];

    return observations
      .filter((obs) => obs.value !== '.')  // 欠損値を除外
      .map((obs) => ({
        date: obs.date,
        value: parseFloat(obs.value)
      }))
      .reverse();  // 古い順に並び替え
  } catch (error) {
    console.error(`Error fetching FRED data for ${seriesId}:`, error);
    return [];
  }
}

export function aggregateMonthlyData(
  data: FredDataPoint[],
  months: number = 24
): Array<{ date: string; value: number }> {
  const monthlyMap = new Map<string, number>();

  data.forEach(point => {
    const yearMonth = point.date.substring(0, 7); // YYYY-MM
    if (!monthlyMap.has(yearMonth)) {
      monthlyMap.set(yearMonth, point.value);
    }
  });

  const sortedMonths = Array.from(monthlyMap.entries())
    .sort((a, b) => a[0].localeCompare(b[0]))
    .slice(-months);

  return sortedMonths.map(([yearMonth, value]) => ({
    date: formatDate(yearMonth + '-01'),
    value
  }));
}
```

#### ステップ6: ダミーデータを実データに置き換え

**ファイル**: `app/page.tsx`

```typescript
'use client';
import { useEffect, useState } from 'react';
import { fetchFredData, aggregateMonthlyData } from '@/lib/fred';

export default function Home() {
  const [cpiData, setCpiData] = useState<ChartData[]>([]);
  const [unemploymentData, setUnemploymentData] = useState<ChartData[]>([]);
  const [treasury10YData, setTreasury10YData] = useState<ChartData[]>([]);
  const [treasury3MData, setTreasury3MData] = useState<ChartData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [cpi, unemployment, treasury10Y, treasury3M] = await Promise.all([
          fetchFredData('CPIAUCSL', 100),
          fetchFredData('UNRATE', 100),
          fetchFredData('DGS10', 100),
          fetchFredData('DGS3MO', 100),
        ]);

        setCpiData(aggregateMonthlyData(cpi, 24));
        setUnemploymentData(aggregateMonthlyData(unemployment, 24));
        setTreasury10YData(aggregateMonthlyData(treasury10Y, 24));
        setTreasury3MData(aggregateMonthlyData(treasury3M, 24));
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  // ... レンダリング部分
}
```

**FRED シリーズID**:
- **CPIAUCSL**: Consumer Price Index (物価指数)
- **UNRATE**: Unemployment Rate (失業率)
- **DGS10**: 10-Year Treasury Constant Maturity Rate (10年国債利回り)
- **DGS3MO**: 3-Month Treasury Bill (3ヶ月国債利回り)

---

### 8. Vercelへのデプロイ（10月7日完了）

#### なぜVercelなのか？

**Vercel**は、Next.jsを開発した会社が提供するホスティングサービス
- ✅ Next.jsに最適化されている
- ✅ 無料プランがある
- ✅ GitHubと自動連携（CI/CD）
- ✅ 環境変数の管理が簡単
- ✅ HTTPSが自動設定される

#### デプロイ手順

##### ステップ1: セキュリティチェック
```bash
# .gitignore に .env.local が含まれているか確認
cat .gitignore | grep .env.local
```

**重要**: APIキーをGitHubにプッシュしないこと！

##### ステップ2: GitHubリポジトリ作成
```bash
# 既存のGitリポジトリを確認
git status

# GitHubに新しいリポジトリを作成（ブラウザで）
# リポジトリ名: fred-dashboard
# 公開設定: Public（練習用なので問題ない）

# リモートを追加してプッシュ
git remote add origin https://github.com/nobusama/fred-dashboard.git
git branch -M main
git push -u origin main
```

**結果**: https://github.com/nobusama/fred-dashboard

##### ステップ3: Vercelアカウント作成
1. https://vercel.com にアクセス
2. 「Sign in with Google」を選択
3. アカウント名: "Nobusama"
4. プラン: Hobby（無料）

**セキュリティに関する質問**:
- Q: "Sign in with Google" は安全？
- A: はい、Vercelは信頼できるサービス。Google OAuth を使うので、パスワードをVercelに渡さない。

##### ステップ4: プロジェクトをインポート
1. Vercelダッシュボードで「Import Git Repository」
2. GitHubアプリをインストール
3. `fred-dashboard` リポジトリを選択
4. 「Import」ボタンをクリック

##### ステップ5: デプロイ設定
```
Project Name: fred-dashboard
Framework Preset: Next.js（自動検出）
Root Directory: ./
Build Command: npm run build（デフォルト）
Output Directory: .next（デフォルト）
```

**環境変数の設定**:
```
Key: NEXT_PUBLIC_FRED_API_KEY
Value: b5cf166e62de7b5801024e71bac57823
```

**重要**: 環境変数をVercelで設定することで、セキュアにAPIキーを管理できる

##### ステップ6: デプロイ実行

「Deploy」ボタンをクリック

**最初のデプロイ**: ビルドエラー発生 ❌
```
Error: Unexpected any. Specify a different type.
41:21  Error: Unexpected any. Specify a different type.
42:18  Error: Unexpected any. Specify a different type.
```

**原因**: TypeScriptの厳格な型チェックで `any` 型が使われていた

**修正**:
```typescript
// 修正前
.filter((obs: any) => obs.value !== '.')
.map((obs: any) => ({ ... }))

// 修正後
interface FredObservation {
  date: string;
  value: string;
}

const observations: FredObservation[] = data.observations || [];
observations
  .filter((obs) => obs.value !== '.')
  .map((obs) => ({ ... }))
```

```bash
git add lib/fred.ts
git commit -m "Fix TypeScript errors in fred.ts"
git push
```

**自動再デプロイ**: Vercelが変更を検知して自動的に再ビルド ✅

##### ステップ7: デプロイ成功！

**公開URL**: https://fred-dashboard-i4do.vercel.app

**確認事項**:
- ✅ ダッシュボードが表示される
- ✅ リアルタイムFREDデータが取得されている
- ✅ 4つのグラフがすべて動作している
- ✅ Last Updated: 10/7/2025

---

### 9. CI/CD（自動デプロイ）の仕組み

#### CI/CD とは？

**CI (Continuous Integration)**:
- コードをpushするたびに自動テスト・ビルド
- エラーがあればすぐに通知

**CD (Continuous Deployment)**:
- テストに合格したら自動的に本番環境へデプロイ

#### Vercelの自動デプロイフロー

```
1. ローカルでコード修正
   ↓
2. git push（GitHubにプッシュ）
   ↓
3. GitHubがVercelに通知（Webhook）
   ↓
4. Vercelが自動的に：
   - コードをダウンロード
   - npm install（依存関係インストール）
   - npm run build（ビルド）
   - デプロイ
   ↓
5. 公開URLが自動更新（1-2分）
```

#### 従来の手動デプロイとの比較

**従来の方法**:
```
1. コードを修正
2. 手動でサーバーにログイン
3. ファイルをアップロード
4. サーバーを再起動
5. 動作確認
→ 30分〜1時間
```

**Vercelの自動デプロイ**:
```
1. コードを修正
2. git push
→ 1-2分で自動デプロイ完了！
```

#### メリット

1. **手間が減る**: pushするだけ
2. **ミスが減る**: 自動化されているので手順を忘れない
3. **履歴管理**: 各デプロイの記録が残る
4. **ロールバック**: 前のバージョンに簡単に戻せる
5. **プレビュー**: ブランチごとにプレビュー環境が作れる

---

### 10. robots.txt による検索エンジン対策

#### なぜ必要？

このダッシュボードは**練習用**なので、Google検索で見つかって欲しくない

#### robots.txt とは？

**検索エンジンのクローラー（ロボット）への指示書**

Googleなどの検索エンジンは、**クローラー**という自動プログラムで：
1. インターネット中のサイトを巡回
2. ページ内容を読み取る
3. 検索結果に登録（インデックス）

robots.txt = 「ここは読まないでください」という看板

#### 設定内容

**ファイル**: `public/robots.txt`

```txt
User-agent: *
Disallow: /
```

**意味**:
- `User-agent: *` → すべてのクローラーに対して
- `Disallow: /` → すべてのページを読み取り禁止

**日本語訳**: 「すべての検索エンジンさん、このサイト全体を検索結果に載せないでください」

#### 効果と限界

**✅ できること**:
- 検索エンジンの結果に出なくする
- 偶然の発見を防ぐ

**❌ できないこと**:
- 完全なアクセス制限ではない
- URLを知っている人は普通にアクセスできる
- パスワード保護ではない

**例え**:
```
robots.txt = 「立入禁止」の看板
           → 守るかどうかは相手次第

パスワード保護 = 鍵のかかったドア
                → 物理的に入れない
```

#### デプロイ

```bash
git add public/robots.txt
git commit -m "Add robots.txt to prevent search engine indexing"
git push
```

→ Vercelが自動的に再デプロイ

**結果**:
- ✅ https://fred-dashboard-i4do.vercel.app/robots.txt でアクセス可能
- ✅ Google検索に出なくなる
- ✅ URLを知っている人だけが見れる

---

### 11. キーポイント

#### このレッスンで最も重要なこと

1. **デザイン → コードの自動生成**
   - 画像を見せるだけで、実装できる
   - 従来は数日 → 数分に短縮

2. **MCP サーバーの活用**
   - Claude Codeと外部ツールを連携
   - 自動化の幅が広がる

3. **2段階アプローチ**
   - 見た目とデータを分けて実装
   - デバッグしやすい

4. **Playwrightによる自動確認**
   - 手動確認から自動確認へ
   - 継続的な品質保証

---

### 9. 感想・気づき

#### Claude Code時代の開発

**変化**:
```
従来: エンジニアが全部コードを書く
今: Claude Codeが大部分を書く、エンジニアは指示と確認
```

**必要なスキル**:
```
従来: プログラミング言語の深い知識
今: 「何を作りたいか」を明確に伝える力
```

**学習方法**:
```
従来: 学んでから使う
今: 使いながら学ぶ
```

---

### 10. 参考リンク

- **FRED API**: https://fred.stlouisfed.org/docs/api/api_key.html
- **Next.js公式**: https://nextjs.org/
- **Playwright公式**: https://playwright.dev/
- **Recharts公式**: https://recharts.org/

---

### 11. 用語集

| 用語 | 説明 |
|------|------|
| **Next.js** | Reactベースのフレームワーク。Webアプリを簡単に作れる |
| **MCP Server** | Claude Codeと外部ツールをつなぐ仕組み |
| **Playwright** | ブラウザ自動化ツール |
| **Recharts** | React用グラフライブラリ |
| **FRED** | Federal Reserve Economic Data（米国経済データAPI） |
| **API Key** | APIを使うための認証キー |
| **ダミーデータ** | テスト用の偽データ |
| **TypeScript** | JavaScriptに型をつけた言語 |
| **Tailwind CSS** | CSSフレームワーク |

---

## 次回の準備

**やっておくこと**:
1. FRED APIアカウント作成
2. APIキーを取得
3. APIキーをメモしておく

**所要時間**: 5分程度

---

## 進捗状況

- ✅ Next.jsプロジェクト作成
- ✅ Playwright MCP Server設定
- ✅ デザイン画像取得
- ✅ ダミーデータでダッシュボード作成
- ✅ FRED API連携（CORS問題解決含む）
- ✅ GitHubリポジトリ作成とプッシュ
- ✅ Vercelアカウント作成
- ✅ 環境変数設定
- ✅ デプロイ（TypeScriptエラー修正含む）
- ✅ robots.txt追加

**完了率**: 100% 🎉

---

## 最終成果物

**公開URL**: https://fred-dashboard-i4do.vercel.app

**GitHubリポジトリ**: https://github.com/nobusama/fred-dashboard

**機能**:
- ✅ リアルタイム経済データ表示（FRED API連携）
- ✅ 4つのインタラクティブグラフ
- ✅ レスポンシブデザイン
- ✅ 自動デプロイ（CI/CD）
- ✅ 検索エンジン対策（robots.txt）

**技術スタック**:
- Next.js 15.5.4 + TypeScript
- Recharts（データ可視化）
- Tailwind CSS（スタイリング）
- FRED API（経済データ）
- Vercel（ホスティング）
- GitHub（バージョン管理）

---

## 学びの総括

### Claude Code時代の開発の特徴

**従来の開発**:
```
1. 要件定義 → 設計 → 実装 → テスト → デプロイ
2. 各ステップで専門知識が必要
3. 数週間〜数ヶ月かかる
```

**Claude Code時代の開発**:
```
1. デザイン画像を見せる
2. Claude Codeが実装
3. リアルデータに接続
4. デプロイ
→ 数時間で完成
```

### 重要な概念の理解

1. **CORS（Cross-Origin Resource Sharing）**
   - ブラウザのセキュリティ機能
   - 解決方法: API Routeでサーバーサイドプロキシ

2. **CI/CD（Continuous Integration/Deployment）**
   - git push するだけで自動デプロイ
   - 手動作業の削減とミス防止

3. **環境変数管理**
   - APIキーなどの秘密情報を安全に管理
   - `.env.local` でローカル環境
   - Vercelで本番環境

4. **robots.txt**
   - 検索エンジンへの指示
   - プライバシー保護（練習用サイト）

### 実際のプロジェクトへの応用

**例：研究データのダッシュボード化**
```
1. Jupyter Notebookでデータ分析
2. 分析結果をどう見せたいか、デザインを用意
3. Claude Codeに実装を依頼
4. 実データと接続
5. Vercelにデプロイ
→ チーム全体で共有！
```

**メリット**:
- 非エンジニアでもダッシュボードが作れる
- インタラクティブな可視化
- URLで簡単に共有
- 常に最新データを表示

---

お疲れ様でした！🎉

Lesson 8 完了です！
