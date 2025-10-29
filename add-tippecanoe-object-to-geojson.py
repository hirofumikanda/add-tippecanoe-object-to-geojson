#!/usr/bin/env python3
"""
tippecanoeオブジェクトをGeoJSONファイルに追加するスクリプト
大きなJSONオブジェクトでも安全に処理できるようにストリーミング処理を使用
"""

import json
import sys
import argparse


def process_geojson_stream(input_file, output_file):
    """
    GeoJSONファイルをストリーミング処理でtippecanoeオブジェクトを追加
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:
            
            for line_num, line in enumerate(infile, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    # JSONオブジェクトをパース
                    feature = json.loads(line)
                    
                    # propertiesが存在する場合のみ処理
                    if 'properties' in feature and feature['properties']:
                        properties = feature['properties']
                        
                        # tippecanoeオブジェクトを作成
                        tippecanoe = {
                            'minzoom': int(properties.get('minzoom', 0)),
                            'maxzoom': int(properties.get('maxzoom', 22))
                        }
                        
                        # layerプロパティが存在する場合は追加
                        if 'layer' in properties:
                            tippecanoe['layer'] = properties['layer']
                        
                        # tippecanoeオブジェクトを追加
                        feature['tippecanoe'] = tippecanoe
                        
                        # minzoom、maxzoom、layerをpropertiesから削除
                        if 'minzoom' in properties:
                            del properties['minzoom']
                        if 'maxzoom' in properties:
                            del properties['maxzoom']
                        if 'layer' in properties:
                            del properties['layer']
                    
                    # 処理済みのfeatureを出力
                    outfile.write(json.dumps(feature, ensure_ascii=False) + '\n')
                    
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON on line {line_num}: {e}", file=sys.stderr)
                    sys.exit(1)
                except Exception as e:
                    print(f"Error processing line {line_num}: {e}", file=sys.stderr)
                    sys.exit(1)
    
    except FileNotFoundError as e:
        print(f"File not found: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Add tippecanoe object to GeoJSON features')
    parser.add_argument('input_file', help='Input GeoJSON file path')
    parser.add_argument('output_file', help='Output GeoJSON file path')
    
    args = parser.parse_args()
    
    process_geojson_stream(args.input_file, args.output_file)
    print("Tippecanoe objects added successfully!", file=sys.stderr)


if __name__ == '__main__':
    main()
