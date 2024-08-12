# Add new recommended extensions

```bash
code --list-extensions > installed_extensions.txt
```

```bash
cat installed_extensions.txt | awk '{print "        \"" $0 "\","}' > recommended_extensions.json

```