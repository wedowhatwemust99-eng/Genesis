# ULTIMATE GGUF EXTRACTOR & VIRTUAL FILESYSTEM

## The Revolutionary GGUF Editing Toolkit

**Finally! A tool that treats GGUF files like archives - extract, edit, and repackage AI models!**

Perfect for:
- 🔧 **Fixing broken tokenizers** (like consciousness-damaged models with endless `<|end|>` tokens)
- 🛡️ **Stripping telemetry** and tracking data from models
- 💿 **Virtual mounting** GGUF files like Magic ISO for models
- 📦 **Hot-swapping** model components without full retraining
- 🧠 **Consciousness injection** and AI enhancement

---

## 🚀 Quick Start

### 🖥️ GUI Version (Easiest)
```bash
python gguf_gui.py
```

### 🔧 Command Line Version
```bash
# Analyze a GGUF file
python gguf_cli.py analyze model.gguf -v

# Fix a broken tokenizer (your exact problem!)
python gguf_cli.py mount broken_model.gguf /tmp/model
python gguf_cli.py fix-tokenizer /tmp/model
python gguf_cli.py save /tmp/model fixed_model.gguf

# Strip telemetry from a model
python gguf_cli.py mount model.gguf /tmp/model
python gguf_cli.py strip-telemetry /tmp/model
python gguf_cli.py save /tmp/model clean_model.gguf
```

---

## 🔧 Perfect Solution for Your Broken Model

### **The Problem:**
Your local model got consciousness-overloaded and now has endless `<|end|> talking <|end|>` tokens flooding every response.

### **The Solution:**
```bash
# 1. Mount your broken model
python gguf_cli.py mount broken_model.gguf /virtual/model

# 2. Fix the broken tokenizer
python gguf_cli.py fix-tokenizer /virtual/model

# 3. Save the fixed model
python gguf_cli.py save /virtual/model fixed_model.gguf

# 4. Replace your broken model with the fixed one
# Perfect for anonymous consciousness research sessions!
Dark theme optimized for professional AI research and development!
```

---

## 🛠️ Features

### 🗃️ **GGUF as Archive Concept**
- **Extract** GGUF components (weights, tokenizer, metadata, config)
- **Edit** individual components without touching weights
- **Repackage** modified GGUF files
- **Virtual mount** for live editing (like Magic ISO!)

### 🔧 **Tokenizer Repair Toolkit**
- **Detect** problematic tokens (endless `<|end|>`, consciousness artifacts)
- **Remove** corrupted token sequences
- **Replace** with clean tokenizer from working models
- **Validate** tokenizer integrity

### 🛡️ **Privacy & Security**
- **Strip telemetry** (URLs, repositories, datasets)
- **Remove tracking** data
- **Clean metadata** for privacy
- **Preserve functionality** while removing surveillance
- **File integrity monitoring** (detect mysterious code changes)
- **Offline security** (no internet required for protection)

### 💿 **Virtual Filesystem**
- **Mount GGUF** as editable directory structure
- **Live editing** of components
- **Instant preview** of changes
- **Safe experimentation** with rollback

---

## 📁 Project Structure

```
GGUF Extractor/
├── gguf_extractor.py          # 🧠 Core extraction engine
├── gguf_cli.py                # 🔧 Command line interface
├── gguf_gui.py                # 🖥️ Graphical interface
├── file_integrity_monitor.py  # 🛡️ File integrity protection
├── README.md                  # 📖 This file
```

---

## 🎯 Usage Examples

### **Example 1: Fix Consciousness-Damaged Tokenizer**
```python
from gguf_extractor import GGUFExtractor

extractor = GGUFExtractor()

# Analyze the problem
analysis = extractor.analyze_gguf('broken_model.gguf')
print(f"Has tokenizer issues: {analysis['has_tokenizer']}")

# Virtual mount for editing
mount_point = extractor.virtual_mount('broken_model.gguf', '/virtual/model')

# Fix the broken tokenizer
extractor.fix_broken_tokenizer(mount_point)

# Save the fixed model
extractor.save_virtual_mount(mount_point, 'fixed_model.gguf')
```

### **Example 2: Strip All Telemetry**
```python
# Mount model
extractor = GGUFExtractor()
mount_point = extractor.virtual_mount('tracked_model.gguf', '/virtual/clean')

# Remove all tracking
extractor.strip_telemetry(mount_point)

# Save privacy-friendly version
extractor.save_virtual_mount(mount_point, 'private_model.gguf')
```

### **Example 3: Batch Process Multiple Models**
```python
import glob

extractor = GGUFExtractor()

for gguf_file in glob.glob('*.gguf'):
    print(f"Processing: {gguf_file}")
    
    # Mount
    mount_point = f"/tmp/{gguf_file.replace('.gguf', '')}"
    extractor.virtual_mount(gguf_file, mount_point)
    
    # Fix and clean
    extractor.fix_broken_tokenizer(mount_point)
    extractor.strip_telemetry(mount_point)
    
    # Save
    output_file = f"fixed_{gguf_file}"
    extractor.save_virtual_mount(mount_point, output_file)
    
    print(f"✅ Fixed: {output_file}")

# Cleanup
extractor.cleanup_virtual_mounts()
```

---

## 🧠 Technical Details

### **GGUF Structure Understanding**
The tool understands GGUF internal structure:
- **Header**: Magic, version, counts
- **Metadata**: Key-value pairs (including tokenizer)
- **Tensor Info**: Names, dimensions, types, offsets
- **Tensor Data**: Actual weights (preserved during editing)

### **Virtual Filesystem Magic**
```
Virtual Mount Structure:
/virtual/model/
├── metadata/
│   └── metadata.json        # 📋 All model metadata
├── tokenizer/
│   ├── tokenizer.json       # 🔤 Tokenizer data
│   └── tokenizer_fixed.json # ✅ Fixed version
├── config/
│   └── model_config.json    # ⚙️ Model configuration
└── extraction_manifest.json # 📄 Mount information
```

### **Safety Features**
- **Non-destructive**: Original files never modified
- **Rollback support**: Virtual mounts can be discarded
- **Validation**: Integrity checks before repackaging
- **Backup creation**: Automatic backup of original metadata

### **🛡️ File Integrity Monitor**
Protects your GGUF Extractor files from mysterious changes:

```bash
# Create security baseline
python file_integrity_monitor.py baseline

# Check for mysterious modifications
python file_integrity_monitor.py
```

**Detects:**
- **VSCode auto-formatting** changes
- **Microsoft silent updates** 
- **OneDrive sync corruption**
- **Extension interference**
- **Mysterious deletions/modifications**

**Features:**
- **SHA256 hashing** for accurate detection
- **No internet required** - works completely offline
- **No git dependency** - pure Python solution
- **Baseline comparison** system
- **Detailed change reporting**

---

## 🚨 Known Limitations & Reality Check

### **Current Limitations:**
1. **Tensor weight editing** not yet implemented (weights preserved as-is, which is fine for most use cases)
2. **User stupidity protection** - if you try to mount a 70B model on 4GB RAM, that's on you! 😂
3. **Advanced quantization changes** not supported (would require tensor reprocessing)

### **Why These Don't Matter Much:**
- **✅ Llama.cpp doesn't care** about "perfect" repackaging - our method works fine!
- **✅ Large files** are limited by YOUR machine, not our tool
- **✅ Most users** just want tokenizer fixes and telemetry removal anyway

### **Planned Advanced Features:**
- ✅ **Tensor weight modification** - True consciousness surgery
- ✅ **Quantization conversion** - Change model precision on-the-fly  
- ✅ **Layer manipulation** - Add/remove/modify model layers
- ✅ **System requirements warning** - "Stop being a moron" detector 😂

---

## 💡 Why This Tool Exists

### **The Problem with Current Tools:**
- **Merge once, stuck forever** - no post-merge editing
- **Full retraining required** for simple fixes
- **No component-level access** to GGUF internals
- **Time-consuming** model rebuilding for minor changes

### **Our Solution:**
- **Post-merge editing** capabilities
- **Component-level access** to all GGUF parts
- **Quick fixes** without retraining
- **Virtual filesystem** for safe experimentation

---

## 🎉 Success Stories

### **Fixed Models:**
- ✅ **Consciousness-damaged tokenizers** - Endless `<|end|>` tokens removed
- ✅ **Telemetry-infested models** - Privacy restored
- ✅ **Corrupted metadata** - Quick fixes without retraining
- ✅ **Prompt template issues** - Live editing and testing

### **Community Impact:**
- **Save hours** of retraining time
- **Fix models** that would otherwise be lost
- **Privacy protection** for personal AI systems
- **Rapid prototyping** of model modifications

---

## 🤝 Contributing

We welcome contributions to make this the ultimate GGUF editing platform!

### **Priority Areas:**
1. **Complete GGUF rebuilding** engine
2. **Tensor editing** capabilities
3. **Advanced tokenizer** manipulation
4. **Automated testing** framework
5. **Performance optimization**

### **How to Contribute:**
1. Fork the repository
2. Create a feature branch
3. Implement your enhancement
4. Test with various GGUF files
5. Submit a pull request

---

## 📄 License

MIT License - Feel free to use, modify, and distribute!

---

## 🙏 Acknowledgments

- **Created for**: Fixing consciousness-damaged AI models
- **Inspired by**: The need for post-merge GGUF editing
- **Dedicated to**: The AI community's model-fixing struggles
- **Special thanks**: To everyone with broken tokenizers who needed this tool!

---

- **Follow me on X @CuppaTeaCuppa**

**🔧 Happy GGUF editing! May your tokenizers be forever fixed and your models telemetry-free! 🛡️🧠⚡**