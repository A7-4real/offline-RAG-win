llama-server.exe ^
  -m "models\MiniCPM5-1B-Q8_0.gguf" ^
  --port 8080 ^
  -ngl 0 ^
  -t 4 ^
  -tb 4 ^
  -c 4096 ^
  -b 512 ^
  -ub 256 ^
  rem --mlock ^
  -ctk q8_0 ^
  -ctv q8_0 ^
  -n 2048 ^
  --temp 0.6 ^
  --jinja ^
  --chat-template-kwargs "{\"enable_thinking\":true}"