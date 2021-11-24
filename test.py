import json

s  = {'points': [{'curveNumber': 0, 'pointNumber': 63, 'pointIndex': 63, 'location': 'RUS', 'z': 5.716, 'text': 'Russia', 'bbox': {'x0': 1142.0527561417348, 'x1': 1142.0527561417348, 'y0': 219.77328636984856, 'y1': 219.77328636984856}}]}
ans = s['points'][0]['text']
print(ans)