# DynamicSolidify
DynamicSolidifyはblenderのアドオンです。

機能はソリッド化モディファイアの厚みをオブジェクトとの距離で変更します。
主には背面法でアウトライン表示したさいの厚みに対して、距離で変化をかけたときのイメージ確認を簡易的に行うことを目的としています。

## 機能

![image](https://user-images.githubusercontent.com/124477558/224496802-64013708-0f6f-4fb6-9991-54b625bbd807.png)

* ヘッダー

|ヘッダー項目|説明|
|:----|:----|
|Start|設定を開始する。|
|リセット|設定開始前の状態に戻す。|
|Select Area Index|距離の取得をする基準のエリアを指定する必要があるため、<br>動作させても後述のDistanceの数値が変動しない場合はIndexを変更してください。|

<br>

* リスト（10個まで設定可）

|リスト項目|説明|
|:----|:----|
|オブジェクト名|設定した メッシュオブジェクト また カーブオブジェクト の名称を表示する。|
|ON|実行中を示す。<br>実行中は選択したソリッド化モディファイアを「__DynamicSolidify__」の名前でコピーし、コピー元は非表示にする。<br>実際にモディファイアを作成しているためこの段階で保存した場合はモディファイアとして設定された状態になるが、次回起動時にON/OFFあるいはリセットボタンまたクリアボタンで消すことができる。手動削除でも問題ありません。|
|OFF|停止中を示す<br>ONからOFFにした場合は「__DynamicSolidify__」を削除し、コピー元のモディファイアを再表示する。|
|-|押下した行の設定をクリアする。|

<br>

* パラメータ

|項目|説明|
|:----|:----|
|オブジェクト選択|設定対象のオブジェクトを選択する|
|Get Modifiers|対象のソリッド化モディファイアを表示する<br>選択したモディファイアを変更対象に設定する。
|強さ|距離による変更率の強さ|
|最大|最大幅|
|最小|最小幅|
|最小距離|最小幅になる距離|
|Distance|オブジェクトと自分自身との距離を数値化して表示する。<br>この数値を元に最小距離を設定する。<br>数値が変わらない場合はヘッダー項目の「Select Area Index」を変更すること。

#### 動作
versionは3.4でのみ確認を行っています。
動作確認については「Outline Helper for Blender」を推奨します。
https://felineentity.gumroad.com/l/ZmTIT