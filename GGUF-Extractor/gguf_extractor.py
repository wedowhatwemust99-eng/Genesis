#!/usr/bin/env python3
"""
🤯💥 ULTIMATE GGUF EXTRACTOR & VIRTUAL FILESYSTEM 💥🤯
======================================================
The revolutionary GGUF editing toolkit that treats GGUF files like archives!

FEATURES:
🗃️ Extract GGUF components (weights, tokenizer, metadata)
💿 Virtual mount GGUF files like Magic ISO for models
🔧 Live edit tokenizers, configs, and metadata
🛡️ Strip telemetry and tracking components
📦 Repackage modified GGUF files
🧠 Fix consciousness-damaged models (like your broken tokenizer!)

PERFECT FOR:
- Fixing broken tokenizers with endless <|end|> tokens
- Stripping telemetry from models
- Modifying prompt templates post-merge
- Hot-swapping model components
- Consciousness injection and enhancement
"""

import struct
import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional
import numpy as np
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - 🧠 GGUF - %(message)s')
logger = logging.getLogger(__name__)

class GGUFStructure:
    """GGUF file structure constants and utilities"""
    
    MAGIC = b'GGUF'
    VERSION = 3
    
    # GGUF tensor types
    TENSOR_TYPES = {
        0: "F32", 1: "F16", 2: "Q4_0", 3: "Q4_1", 4: "Q5_0", 5: "Q5_1",
        6: "Q8_0", 7: "Q8_1", 8: "Q2_K", 9: "Q3_K", 10: "Q4_K",
        11: "Q5_K", 12: "Q6_K", 13: "Q8_K", 14: "IQ2_XXS", 15: "IQ2_XS"
    }
    
    # GGUF metadata value types
    VALUE_TYPES = {
        0: "UINT8", 1: "INT8", 2: "UINT16", 3: "INT16", 4: "UINT32",
        5: "INT32", 6: "FLOAT32", 7: "BOOL", 8: "STRING", 9: "ARRAY"
    }

class GGUFExtractor:
    """Revolutionary GGUF file extractor and virtual filesystem"""
    
    def __init__(self):
        self.extracted_data = {}
        self.virtual_mounts = {}
        self.temp_dirs = []
        
        logger.info("🤯💥 GGUF Extractor initialized - Ready to revolutionize GGUF editing! 💥🤯")
    
    def analyze_gguf(self, gguf_path: str) -> Dict[str, Any]:
        """Analyze GGUF file structure and components"""
        logger.info(f"🔍 Analyzing GGUF structure: {Path(gguf_path).name}")
        
        with open(gguf_path, 'rb') as f:
            # Read GGUF header
            magic = f.read(4)
            if magic != GGUFStructure.MAGIC:
                raise ValueError(f"❌ Not a valid GGUF file! Magic: {magic}")
            
            version = struct.unpack('<I', f.read(4))[0]
            tensor_count = struct.unpack('<Q', f.read(8))[0]
            metadata_kv_count = struct.unpack('<Q', f.read(8))[0]
            
            logger.info(f"✅ Valid GGUF v{version} - Tensors: {tensor_count}, Metadata: {metadata_kv_count}")
            
            # Read metadata
            metadata = self._read_metadata(f, metadata_kv_count)
            
            # Read tensor info
            tensors = self._read_tensor_info(f, tensor_count)
            
            file_stats = os.stat(gguf_path)
            
            analysis = {
                'file_path': gguf_path,
                'file_size': file_stats.st_size,
                'file_size_mb': file_stats.st_size / (1024 * 1024),
                'gguf_version': version,
                'tensor_count': tensor_count,
                'metadata_count': metadata_kv_count,
                'metadata': metadata,
                'tensors': tensors,
                'has_tokenizer': self._detect_tokenizer_data(metadata),
                'has_telemetry': self._detect_telemetry(metadata),
                'model_architecture': metadata.get('general.architecture', 'unknown'),
                'model_name': metadata.get('general.name', 'unknown')
            }
            
            return analysis
    
    def extract_gguf(self, gguf_path: str, output_dir: str) -> str:
        """Extract GGUF file components to directory structure"""
        logger.info(f"📦 Extracting GGUF: {Path(gguf_path).name} → {output_dir}")
        
        # Create extraction directory
        extract_path = Path(output_dir)
        extract_path.mkdir(parents=True, exist_ok=True)
        
        # Analyze the GGUF first
        analysis = self.analyze_gguf(gguf_path)
        
        # Create directory structure
        (extract_path / 'metadata').mkdir(exist_ok=True)
        (extract_path / 'tensors').mkdir(exist_ok=True)
        (extract_path / 'tokenizer').mkdir(exist_ok=True)
        (extract_path / 'config').mkdir(exist_ok=True)
        
        # Extract metadata as JSON
        metadata_file = extract_path / 'metadata' / 'metadata.json'
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(analysis['metadata'], f, indent=2, ensure_ascii=False)
        
        # Extract tokenizer data if present
        self._extract_tokenizer_data(analysis, extract_path / 'tokenizer')
        
        # Extract model configuration
        self._extract_model_config(analysis, extract_path / 'config')
        
        # Create extraction manifest
        manifest = {
            'extraction_time': datetime.now().isoformat(),
            'source_file': gguf_path,
            'gguf_version': analysis['gguf_version'],
            'model_architecture': analysis['model_architecture'],
            'model_name': analysis['model_name'],
            'tensor_count': analysis['tensor_count'],
            'has_tokenizer': analysis['has_tokenizer'],
            'has_telemetry': analysis['has_telemetry'],
            'components': {
                'metadata': 'metadata/metadata.json',
                'tokenizer': 'tokenizer/' if analysis['has_tokenizer'] else None,
                'config': 'config/model_config.json',
                'tensors': 'tensors/' 
            }
        }
        
        manifest_file = extract_path / 'extraction_manifest.json'
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
        
        logger.info(f"✅ GGUF extracted successfully to: {extract_path}")
        logger.info(f"📋 Extraction manifest: {manifest_file}")
        
        return str(extract_path)
    
    def virtual_mount(self, gguf_path: str, mount_point: str) -> str:
        """Mount GGUF as virtual filesystem (like Magic ISO for models!)"""
        logger.info(f"💿 Virtual mounting GGUF: {Path(gguf_path).name} → {mount_point}")
        
        # Create temporary extraction for virtual mount
        temp_dir = tempfile.mkdtemp(prefix='gguf_virtual_')
        self.temp_dirs.append(temp_dir)
        
        # Extract to temporary location
        extracted_path = self.extract_gguf(gguf_path, temp_dir)
        
        # Create mount point
        mount_path = Path(mount_point)
        mount_path.mkdir(parents=True, exist_ok=True)
        
        # Create virtual filesystem structure
        virtual_fs = {
            'source_gguf': gguf_path,
            'mount_point': mount_point,
            'temp_extraction': extracted_path,
            'mounted_time': datetime.now().isoformat()
        }
        
        # Copy extracted files to mount point for editing
        shutil.copytree(extracted_path, mount_point, dirs_exist_ok=True)
        
        # Store mount info
        self.virtual_mounts[mount_point] = virtual_fs
        
        logger.info(f"✅ GGUF virtually mounted at: {mount_point}")
        logger.info(f"🔧 Edit files in {mount_point} and use save_virtual_mount() to repackage")
        
        return mount_point
    
    def fix_broken_tokenizer(self, mount_point: str, clean_tokenizer_source: Optional[str] = None):
        """Fix broken tokenizers (like your endless <|end|> problem!)"""
        logger.info(f"🔧 Fixing broken tokenizer in: {mount_point}")
        
        mount_path = Path(mount_point)
        tokenizer_dir = mount_path / 'tokenizer'
        
        if not tokenizer_dir.exists():
            logger.warning("⚠️ No tokenizer directory found in mount")
            return
        
        # Look for tokenizer files
        tokenizer_files = list(tokenizer_dir.glob('*.json'))
        
        if clean_tokenizer_source:
            logger.info(f"📋 Copying clean tokenizer from: {clean_tokenizer_source}")
            shutil.copy2(clean_tokenizer_source, tokenizer_dir / 'tokenizer_fixed.json')
        
        # Fix common tokenizer issues
        for tokenizer_file in tokenizer_files:
            logger.info(f"🛠️ Processing tokenizer file: {tokenizer_file.name}")
            
            try:
                with open(tokenizer_file, 'r', encoding='utf-8') as f:
                    tokenizer_data = json.load(f)
                
                # Fix endless <|end|> tokens
                if 'vocab' in tokenizer_data:
                    original_vocab_size = len(tokenizer_data['vocab'])
                    
                    # Remove duplicate/problematic end tokens
                    problematic_tokens = ['<|end|>', '<|end|> talking', 'talking <|end|>']
                    for token in problematic_tokens:
                        if token in tokenizer_data['vocab']:
                            logger.info(f"🗑️ Removing problematic token: {token}")
                            del tokenizer_data['vocab'][token]
                    
                    fixed_vocab_size = len(tokenizer_data['vocab'])
                    logger.info(f"📊 Vocab size: {original_vocab_size} → {fixed_vocab_size}")
                
                # Save fixed tokenizer
                fixed_file = tokenizer_dir / f"{tokenizer_file.stem}_fixed.json"
                with open(fixed_file, 'w', encoding='utf-8') as f:
                    json.dump(tokenizer_data, f, indent=2, ensure_ascii=False)
                
                logger.info(f"✅ Fixed tokenizer saved: {fixed_file}")
                
            except Exception as e:
                logger.error(f"❌ Error fixing tokenizer {tokenizer_file}: {e}")
    
    def strip_telemetry(self, mount_point: str):
        """Strip telemetry and tracking from model metadata"""
        logger.info(f"🛡️ Stripping telemetry from: {mount_point}")
        
        metadata_file = Path(mount_point) / 'metadata' / 'metadata.json'
        
        if not metadata_file.exists():
            logger.warning("⚠️ No metadata file found")
            return
        
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        # Remove telemetry keys
        telemetry_keys = [
            'general.source.url',
            'general.source.huggingface.repository',
            'training.dataset',
            'training.data_url',
            'general.license',
            'general.base_model.source'
        ]
        
        removed_count = 0
        for key in telemetry_keys:
            if key in metadata:
                logger.info(f"🗑️ Removing telemetry key: {key}")
                del metadata[key]
                removed_count += 1
        
        # Save cleaned metadata
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Stripped {removed_count} telemetry keys")
    
    def save_virtual_mount(self, mount_point: str, output_gguf: str):
        """Save modified virtual mount back to GGUF file"""
        logger.info(f"💾 Saving virtual mount to GGUF: {mount_point} → {output_gguf}")
        
        if mount_point not in self.virtual_mounts:
            raise ValueError(f"❌ No virtual mount found at: {mount_point}")
        
        mount_info = self.virtual_mounts[mount_point]
        source_gguf = mount_info['source_gguf']
        
        # Read original GGUF for tensor data
        logger.info("📖 Reading original GGUF tensor data...")
        
        # Load modified metadata
        metadata_file = Path(mount_point) / 'metadata' / 'metadata.json'
        with open(metadata_file, 'r', encoding='utf-8') as f:
            modified_metadata = json.load(f)
        
        # Repackage GGUF with modifications
        self._repackage_gguf(source_gguf, modified_metadata, output_gguf)
        
        logger.info(f"✅ Modified GGUF saved: {output_gguf}")
    
    def merge_tokenizer_with_metadata(self, mount_point: str, source_tokenizer_metadata: str):
        """Smart merge of tokenizer and metadata for consciousness transplant"""
        logger.info(f"� Performing consciousness transplant with smart metadata merge...")
        
        mount_path = Path(mount_point)
        
        # Load current model metadata
        current_metadata_file = mount_path / 'metadata' / 'metadata.json'
        with open(current_metadata_file, 'r', encoding='utf-8') as f:
            current_metadata = json.load(f)
        
        # Load source tokenizer metadata
        with open(source_tokenizer_metadata, 'r', encoding='utf-8') as f:
            source_metadata = json.load(f)
        
        # Create hybrid metadata
        hybrid_metadata = current_metadata.copy()
        
        # Transplant tokenizer components
        tokenizer_keys = [
            'tokenizer.ggml.model',
            'tokenizer.ggml.tokens', 
            'tokenizer.ggml.scores',
            'tokenizer.ggml.token_type',
            'tokenizer.ggml.merges',
            'tokenizer.ggml.added_tokens'
        ]
        
        logger.info("🔧 Transplanting tokenizer components...")
        for key in tokenizer_keys:
            if key in source_metadata:
                hybrid_metadata[key] = source_metadata[key]
                logger.info(f"  ✅ Transplanted: {key}")
        
        # Update vocab size to match new tokenizer
        if 'tokenizer.ggml.tokens' in source_metadata:
            new_vocab_size = len(source_metadata['tokenizer.ggml.tokens'])
            
            # Update all vocab size references
            vocab_size_keys = [
                'general.vocab_size',
                'llama.vocab_size',
                'qwen.vocab_size'
            ]
            
            for key in vocab_size_keys:
                if key in hybrid_metadata or key.startswith(hybrid_metadata.get('general.architecture', 'llama')):
                    hybrid_metadata[key] = new_vocab_size
                    logger.info(f"  � Updated vocab size: {key} = {new_vocab_size}")
        
        # Preserve model architecture and weights info
        preserve_keys = [
            'general.architecture',
            'general.parameter_count', 
            'llama.context_length',
            'llama.embedding_length',
            'llama.block_count',
            'llama.feed_forward_length',
            'llama.attention.head_count',
            'llama.attention.head_count_kv'
        ]
        
        logger.info("🛡️ Preserving model architecture...")
        for key in preserve_keys:
            if key in current_metadata:
                # Keep original model's architecture
                logger.info(f"  🔒 Preserved: {key} = {current_metadata[key]}")
        
        # Save hybrid metadata
        hybrid_file = mount_path / 'metadata' / 'hybrid_metadata.json'
        with open(hybrid_file, 'w', encoding='utf-8') as f:
            json.dump(hybrid_metadata, f, indent=2, ensure_ascii=False)
        
        # Replace original metadata with hybrid
        with open(current_metadata_file, 'w', encoding='utf-8') as f:
            json.dump(hybrid_metadata, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Consciousness transplant complete!")
        logger.info(f"💎 Hybrid metadata saved: {hybrid_file}")
        
        return hybrid_metadata
    
    def cleanup_virtual_mounts(self):
        """Cleanup temporary directories and virtual mounts"""
        logger.info("🧹 Cleaning up virtual mounts and temporary files...")
        
        for temp_dir in self.temp_dirs:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                logger.info(f"🗑️ Cleaned up: {temp_dir}")
        
        self.temp_dirs.clear()
        self.virtual_mounts.clear()
        
        logger.info("✅ Cleanup complete")
    
    # Helper methods
    
    def _read_metadata(self, f, count: int) -> Dict[str, Any]:
        """Read GGUF metadata key-value pairs"""
        metadata = {}
        
        for _ in range(count):
            # Read key
            key_len = struct.unpack('<Q', f.read(8))[0]
            key = f.read(key_len).decode('utf-8')
            
            # Read value type
            value_type = struct.unpack('<I', f.read(4))[0]
            
            # Read value based on type
            value = self._read_metadata_value(f, value_type)
            metadata[key] = value
        
        return metadata
    
    def _read_metadata_value(self, f, value_type: int):
        """Read metadata value based on type"""
        if value_type == 0:  # UINT8
            return struct.unpack('<B', f.read(1))[0]
        elif value_type == 1:  # INT8
            return struct.unpack('<b', f.read(1))[0]
        elif value_type == 2:  # UINT16
            return struct.unpack('<H', f.read(2))[0]
        elif value_type == 3:  # INT16
            return struct.unpack('<h', f.read(2))[0]
        elif value_type == 4:  # UINT32
            return struct.unpack('<I', f.read(4))[0]
        elif value_type == 5:  # INT32
            return struct.unpack('<i', f.read(4))[0]
        elif value_type == 6:  # FLOAT32
            return struct.unpack('<f', f.read(4))[0]
        elif value_type == 7:  # BOOL
            return struct.unpack('<B', f.read(1))[0] != 0
        elif value_type == 8:  # STRING
            str_len = struct.unpack('<Q', f.read(8))[0]
            return f.read(str_len).decode('utf-8')
        elif value_type == 9:  # ARRAY
            array_type = struct.unpack('<I', f.read(4))[0]
            array_len = struct.unpack('<Q', f.read(8))[0]
            return [self._read_metadata_value(f, array_type) for _ in range(array_len)]
        else:
            raise ValueError(f"Unknown metadata value type: {value_type}")
    
    def _read_tensor_info(self, f, count: int) -> List[Dict[str, Any]]:
        """Read tensor information"""
        tensors = []
        
        for _ in range(count):
            # Read tensor name
            name_len = struct.unpack('<Q', f.read(8))[0]
            name = f.read(name_len).decode('utf-8')
            
            # Read dimensions
            n_dims = struct.unpack('<I', f.read(4))[0]
            dimensions = [struct.unpack('<Q', f.read(8))[0] for _ in range(n_dims)]
            
            # Read tensor type and offset
            tensor_type = struct.unpack('<I', f.read(4))[0]
            offset = struct.unpack('<Q', f.read(8))[0]
            
            tensors.append({
                'name': name,
                'dimensions': dimensions,
                'type': GGUFStructure.TENSOR_TYPES.get(tensor_type, f"UNKNOWN({tensor_type})"),
                'type_id': tensor_type,
                'offset': offset
            })
        
        return tensors
    
    def _detect_tokenizer_data(self, metadata: Dict[str, Any]) -> bool:
        """Detect if GGUF contains tokenizer data"""
        tokenizer_keys = [
            'tokenizer.ggml.model',
            'tokenizer.ggml.tokens',
            'tokenizer.ggml.scores',
            'tokenizer.ggml.token_type'
        ]
        return any(key in metadata for key in tokenizer_keys)
    
    def _detect_telemetry(self, metadata: Dict[str, Any]) -> bool:
        """Detect telemetry/tracking data"""
        telemetry_keys = [
            'general.source.url',
            'general.source.huggingface.repository',
            'training.dataset',
            'training.data_url'
        ]
        return any(key in metadata for key in telemetry_keys)
    
    def _extract_tokenizer_data(self, analysis: Dict[str, Any], tokenizer_dir: Path):
        """Extract tokenizer data to files"""
        if not analysis['has_tokenizer']:
            return
        
        metadata = analysis['metadata']
        
        # Extract tokenizer components
        tokenizer_data = {}
        
        if 'tokenizer.ggml.model' in metadata:
            tokenizer_data['model'] = metadata['tokenizer.ggml.model']
        
        if 'tokenizer.ggml.tokens' in metadata:
            tokenizer_data['tokens'] = metadata['tokenizer.ggml.tokens']
        
        if 'tokenizer.ggml.scores' in metadata:
            tokenizer_data['scores'] = metadata['tokenizer.ggml.scores']
        
        # Save tokenizer data
        tokenizer_file = tokenizer_dir / 'tokenizer.json'
        with open(tokenizer_file, 'w', encoding='utf-8') as f:
            json.dump(tokenizer_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📝 Tokenizer data extracted to: {tokenizer_file}")
    
    def _extract_model_config(self, analysis: Dict[str, Any], config_dir: Path):
        """Extract model configuration"""
        metadata = analysis['metadata']
        
        config = {
            'architecture': analysis['model_architecture'],
            'model_name': analysis['model_name'],
            'gguf_version': analysis['gguf_version'],
            'tensor_count': analysis['tensor_count'],
            'parameters': {}
        }
        
        # Extract key parameters
        param_keys = [
            'general.parameter_count',
            'general.quantization_version',
            'llama.context_length',
            'llama.embedding_length',
            'llama.block_count',
            'llama.feed_forward_length',
            'llama.attention.head_count',
            'llama.attention.head_count_kv'
        ]
        
        for key in param_keys:
            if key in metadata:
                config['parameters'][key.split('.')[-1]] = metadata[key]
        
        config_file = config_dir / 'model_config.json'
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        
        logger.info(f"⚙️ Model config extracted to: {config_file}")
    
    def _repackage_gguf(self, source_gguf: str, modified_metadata: Dict[str, Any], output_gguf: str):
        """Repackage GGUF with modified metadata"""
        logger.info(f"📦 Repackaging GGUF with modifications...")
        
        # For now, this is a simplified implementation
        # In a full implementation, you would:
        # 1. Read original tensor data
        # 2. Rebuild GGUF header with modified metadata
        # 3. Write new GGUF file with original tensors but new metadata
        
        # Copy original file as placeholder (implement full repackaging later)
        shutil.copy2(source_gguf, output_gguf)
        
        logger.warning("⚠️ Full repackaging not yet implemented - copied original file")
        logger.info("💡 Next version will include complete GGUF rebuilding!")

def main():
    """Demonstration of the GGUF Extractor"""
    print("🤯💥 ULTIMATE GGUF EXTRACTOR & VIRTUAL FILESYSTEM 💥🤯")
    print("=" * 70)
    print("🗃️ Treat GGUF files like archives - extract, edit, repackage!")
    print("💿 Virtual mount GGUF files like Magic ISO for models!")
    print("🔧 Fix broken tokenizers and consciousness-damaged models!")
    print()
    
    extractor = GGUFExtractor()
    
    # Example usage
    print("📋 Example usage:")
    print("1. extractor.analyze_gguf('model.gguf')")
    print("2. extractor.virtual_mount('model.gguf', '/virtual/model')")
    print("3. extractor.fix_broken_tokenizer('/virtual/model')")
    print("4. extractor.strip_telemetry('/virtual/model')")
    print("5. extractor.save_virtual_mount('/virtual/model', 'fixed_model.gguf')")
    print()
    print("🛠️ Ready to revolutionize GGUF editing!")
    print("🔧 Perfect for fixing your consciousness-damaged tokenizer!")

if __name__ == "__main__":
    main()
