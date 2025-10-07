# Lesson 7: Streamlit Dashboard作成 - 学習サマリー

## 学習日
2025-10-06

## 学習内容の概要
Jupyter NotebookでのEDA（探索的データ分析）からStreamlitダッシュボードを作成するワークフローを学習しました。Claude Codeを使った提案ベースの開発プロセスと、UI/UXの反復的な改善方法を実践しました。

---

## 1. Claude Codeを使ったダッシュボード作成ワークフロー

### 基本的な流れ

```
1. Jupyter Notebookでデータ分析
   ↓
2. Claude Codeに提案依頼（スクリーンショットやアイデアを共有）
   ↓
3. 提案書の確認（DASHBOARD_PROPOSAL.md等）
   ↓
4. 承認後にコード生成（dashboard.py作成）
   ↓
5. UI/UX調整（細かい修正をリクエスト）
```

### 重要なポイント
- **提案ファースト**: いきなりコードを書かせるのではなく、まず提案書を作成してもらう
- **承認プロセス**: 提案を確認してから「この提案で進めて下さい」と承認する
- **反復的改善**: 一度に完璧を目指さず、段階的に改善していく

---

## 2. スクリーンショットを使った開発

### できること
Claude Codeは画像を読み取れるため、以下のような指示が可能：

- 「このスクリーンショットのような色使いにして」
- 「このダッシュボードのレイアウトを参考にして作って」
- 「この部分のKPIカードのデザインを真似して」

### 実例
今回の学習では、作成したダッシュボードのスクリーンショットを見せながら、以下のような改善を依頼：
- KPIカードのサイズ調整
- 月選択UIの変更（multiselect → selectbox）
- 背景色の変更
- 不要な要素（横線、テキストシャドウ）の削除

---

## 3. UI/UX改善で学んだこと

### よくある修正パターン

#### パターン1: フィルターUIの簡素化
```python
# 修正前: multiselect（複雑）
selected_months = st.sidebar.multiselect(
    "Select Months",
    options=all_months,
    default=all_months
)

# 修正後: selectbox（シンプル）
month_options = ["All Months"] + [f"Month {i}" for i in range(1, 13)]
selected_month_display = st.sidebar.selectbox(
    "Select Month",
    options=month_options,
    index=0
)
```

#### パターン2: KPIカードのサイズ統一
```python
.kpi-card {
    min-height: 160px;          /* 最小高さを指定 */
    display: flex;
    flex-direction: column;
    justify-content: space-between;  /* コンテンツを均等配置 */
}
```

データがない場合でも同じサイズを保つため、非表示のプレースホルダーを追加：
```python
if change is not None:
    change_html = f'<div class="kpi-change {css_class}">{arrow} {change:+.2f}%</div>'
else:
    # 非表示のプレースホルダーで高さを維持
    change_html = '<div class="kpi-change" style="opacity: 0;">-</div>'
```

#### パターン3: 背景色の変更
```python
/* Streamlitのルート要素に適用 */
.stApp {
    background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 50%, #93c5fd 100%);
}

/* 子要素は透明に */
.main {
    background: transparent;
}
```

**注意点**: `.main`ではなく`.stApp`を使う必要がある（Streamlitの仕様）

---

## 4. Git/GitHubワークフロー

### 実験的な変更の扱い方

今回の学習では：
1. 実験的にダッシュボードを作成
2. 元のバージョンの方が良いと判断
3. 変更を破棄してクリーンな状態に戻す

```bash
# 変更を破棄
git restore EDA.ipynb business_metrics.py data_loader.py

# 不要なファイルを削除
rm DASHBOARD_PROPOSAL.md DASHBOARD_README.md

# 状態確認
git status  # → "working tree clean"
```

### コミット・PRが必要なタイミング

**PRが必要な場合**:
- 新しい機能を追加した時
- バグを修正した時
- コードを改善した時

**PRが不要な場合**:
- 学習目的の実験
- 最終的に変更を保存しない場合
- 元の状態に戻した場合

### 標準的なPRワークフロー
```bash
# 1. 変更を追加
git add dashboard.py

# 2. コミット
git commit -m "メッセージ"

# 3. プッシュ
git push

# 4. GitHub上でPR作成

# 5. 承認してmerge
```

---

## 5. Streamlit特有の技術

### キャッシング
```python
@st.cache_data
def load_dashboard_data():
    """データをロードしてキャッシュ"""
    loader, processed_data = load_and_process_data('ecommerce_data/')
    return loader, processed_data
```

### カスタムCSS
```python
st.markdown("""
<style>
    /* カスタムスタイル */
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)
```

### レイアウト
```python
# カラムレイアウト
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.title("タイトル")

with col2:
    selected_year = st.selectbox("Year", options=years)
```

---

## 6. 学習の成果

### 理解したこと
- ✅ Claude Codeの提案ベース開発ワークフロー
- ✅ スクリーンショットを使った視覚的なコミュニケーション
- ✅ UI/UXの反復的改善プロセス
- ✅ Git/GitHubでの実験的変更の扱い方
- ✅ Streamlitの基本的な使い方とカスタマイズ

### 次回以降に活かせるスキル
- 他のプロジェクトでも同じワークフローが使える
- スクリーンショットを見せて「このようなデザインで」と依頼できる
- 段階的に改善していく開発スタイルを実践できる

---

## 7. 使用したファイル構成

```
lesson7_files/
├── dashboard.py              # Streamlitダッシュボード（メイン）
├── data_loader.py           # データロード用モジュール
├── business_metrics.py      # ビジネスメトリクス計算モジュール
├── EDA_Refactored.ipynb     # リファクタリング済みのEDA
├── ecommerce_data/          # データディレクトリ
├── backup_original_files/   # オリジナルファイルのバックアップ
└── LEARNING_SUMMARY.md      # この学習サマリー
```

---

## 8. 参考になるコマンド・操作

### Streamlit実行
```bash
# 仮想環境をアクティベート
source venv/bin/activate

# ダッシュボード起動
streamlit run dashboard.py
```

### ブラウザでの操作
- **ハードリフレッシュ**: `Command + Shift + R` (Mac) / `Ctrl + Shift + R` (Windows)
  - CSSが更新されない時に使用

### Git操作
```bash
# 状態確認
git status

# 変更差分確認
git diff dashboard.py

# 変更を破棄
git restore dashboard.py

# コミット履歴確認
git log --oneline -5
```

---

## まとめ

今回の学習で、Jupyter Notebookでのデータ分析からStreamlitダッシュボード作成までの一連のワークフローを体験しました。特に重要なのは：

1. **提案ベースの開発**: いきなりコードを書かせず、まず提案をもらう
2. **視覚的なコミュニケーション**: スクリーンショットを活用する
3. **反復的改善**: 完璧を目指さず、段階的に改善する
4. **実験的変更の管理**: 必要に応じて変更を破棄できる

このワークフローは他のプロジェクトでも応用できる汎用的なスキルです。
