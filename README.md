# GeoJSON Tippecanoe オブジェクト追加ツール

このスクリプトは、GeoJSONファイルの各フィーチャーに`tippecanoe`オブジェクトを追加し、プロパティから対応する値を移動させるツールです。

## 動機
- [felt/tippecanoe](https://github.com/felt/tippecanoe)を使用してGeoJSONからMVTを作成する場合、GeoJSONをndjson形式にしておくことで、-Pオプション（並列処理）を使用することができます。
- その際、各フィーチャにtippecanoeオブジェクトを付与することで、レイヤ名（layer）、最大ズームレベル（maxzoom）、最小ズームレベル（minzoom）をフィーチャ個別に設定可能です。Node.jsの[ndjson-cli](https://github.com/mbostock/ndjson-cli/blob/master/README.md)のndjson-mapを使用することで、各フィーチャのプロパティに設定したlayer、maxzoom、minzoomからマッピングしてtippecanoeオブジェクトを付与できます。（上記のtippecanoeのページではその方法が紹介されています。）
- ただし、その場合、内部的にはNode.jsのreadlineで処理することになり、文字数制限が割と厳しいため、一定以上のデータサイズのジオメトリを扱うと、エラーになることがあります。
- そのため、本プロジェクトでは、より柔軟に処理できるpythonスクリプトを作成しました。

## 概要

GeoJSONファイル内のフィーチャーのプロパティに含まれる以下の項目を`tippecanoe`オブジェクトに移動します：

- `minzoom`: 最小ズームレベル（デフォルト: 0）
- `maxzoom`: 最大ズームレベル（デフォルト: 22）
- `layer`: レイヤ名（存在する場合のみ）

ズームレベルのデフォルト値は必要に応じて変更ください。

## 機能

- **ストリーミング処理**: 大きなGeoJSONファイルでも安全に処理
- **エラーハンドリング**: JSONパースエラーやファイルエラーを適切に処理
- **プロパティの移動**: 指定されたプロパティを`properties`から`tippecanoe`オブジェクトに移動

## 使用方法

### 基本的な使用法

```bash
python add-tippecanoe-object-to-geojson.py input.geojson output.geojson
```

### 引数

- `input_file`: 入力GeoJSONファイルのパス
- `output_file`: 出力GeoJSONファイルのパス

## 入力例

```json
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [139.7671, 35.6812]
  },
  "properties": {
    "name": "東京駅",
    "minzoom": 5,
    "maxzoom": 18,
    "layer": "stations"
  }
}
```

## 出力例

```json
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [139.7671, 35.6812]
  },
  "properties": {
    "name": "東京駅"
  },
  "tippecanoe": {
    "minzoom": 5,
    "maxzoom": 18,
    "layer": "stations"
  }
}
```

## 要件

- Python 3.x

## 注意事項

- 入力ファイルは1行に1つのGeoJSONフィーチャーが記載されている形式を想定
- `properties`が存在しないフィーチャーはそのまま出力
- `minzoom`、`maxzoom`、`layer`以外のプロパティは変更されません

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。