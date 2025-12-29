import glob, os, json
os.chdir("Posts")
output = []
for file in glob.glob("*.html"):
    output.append(file)
    
os.chdir("..")
with open("blogs.txt", "w", encoding="utf-8") as fh:
    json.dump(output, fh, indent=2, ensure_ascii=False)