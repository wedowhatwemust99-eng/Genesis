#!/usr/bin/env python3
"""
🔧 GGUF EDITOR CLI - Command Line Interface for GGUF Extractor
============================================================
Easy-to-use CLI for fixing broken tokenizers and editing GGUF files!

USAGE EXAMPLES:
python gguf_cli.py analyze model.gguf
python gguf_cli.py extract model.gguf extracted/
python gguf_cli.py mount model.gguf /virtual/model
python gguf_cli.py fix-tokenizer /virtual/model
python gguf_cli.py strip-telemetry /virtual/model
python gguf_cli.py save /virtual/model fixed_model.gguf
"""

import argparse
import sys
from pathlib import Path
from gguf_extractor import GGUFExtractor
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - 🛠️ CLI - %(message)s')
logger = logging.getLogger(__name__)

def cmd_analyze(args):
    """Analyze GGUF file structure"""
    print(f"🔍 Analyzing GGUF: {args.gguf_file}")
    
    extractor = GGUFExtractor()
    analysis = extractor.analyze_gguf(args.gguf_file)
    
    print("\n📊 GGUF Analysis Results:")
    print("=" * 50)
    print(f"📁 File: {Path(args.gguf_file).name}")
    print(f"📏 Size: {analysis['file_size_mb']:.2f} MB")
    print(f"🏗️ Architecture: {analysis['model_architecture']}")
    print(f"🏷️ Model Name: {analysis['model_name']}")
    print(f"📦 GGUF Version: {analysis['gguf_version']}")
    print(f"🧮 Tensors: {analysis['tensor_count']}")
    print(f"📋 Metadata Keys: {analysis['metadata_count']}")
    print(f"🔤 Has Tokenizer: {'✅ Yes' if analysis['has_tokenizer'] else '❌ No'}")
    print(f"📡 Has Telemetry: {'⚠️ Yes' if analysis['has_telemetry'] else '✅ Clean'}")
    
    if args.verbose:
        print(f"\n📝 Metadata Preview:")
        for key, value in list(analysis['metadata'].items())[:10]:
            print(f"  {key}: {str(value)[:100]}")
        
        print(f"\n🧮 Tensor Preview:")
        for tensor in analysis['tensors'][:5]:
            print(f"  {tensor['name']}: {tensor['type']} {tensor['dimensions']}")

def cmd_extract(args):
    """Extract GGUF to directory"""
    print(f"📦 Extracting GGUF: {args.gguf_file} → {args.output_dir}")
    
    extractor = GGUFExtractor()
    extracted_path = extractor.extract_gguf(args.gguf_file, args.output_dir)
    
    print(f"✅ Extraction complete!")
    print(f"📁 Components extracted to: {extracted_path}")
    print(f"📋 Check extraction_manifest.json for details")

def cmd_mount(args):
    """Virtual mount GGUF file"""
    print(f"💿 Virtual mounting: {args.gguf_file} → {args.mount_point}")
    
    extractor = GGUFExtractor()
    mount_path = extractor.virtual_mount(args.gguf_file, args.mount_point)
    
    print(f"✅ GGUF virtually mounted at: {mount_path}")
    print(f"🔧 Edit files in {mount_path} and use 'save' command to repackage")
    print(f"📁 Available components:")
    print(f"  📋 metadata/metadata.json")
    print(f"  🔤 tokenizer/ (if present)")
    print(f"  ⚙️ config/model_config.json")
    
    # Store mount info for CLI session
    with open('.gguf_cli_mounts.json', 'w') as f:
        json.dump({args.mount_point: args.gguf_file}, f)

def cmd_fix_tokenizer(args):
    """Fix broken tokenizer in mounted GGUF"""
    print(f"🔧 Fixing tokenizer in: {args.mount_point}")
    
    extractor = GGUFExtractor()
    
    clean_source = None
    if args.clean_tokenizer:
        clean_source = args.clean_tokenizer
        print(f"📋 Using clean tokenizer from: {clean_source}")
    
    extractor.fix_broken_tokenizer(args.mount_point, clean_source)
    
    print(f"✅ Tokenizer fix complete!")
    print(f"🔍 Check {args.mount_point}/tokenizer/ for fixed files")

def cmd_strip_telemetry(args):
    """Strip telemetry from mounted GGUF"""
    print(f"🛡️ Stripping telemetry from: {args.mount_point}")
    
    extractor = GGUFExtractor()
    extractor.strip_telemetry(args.mount_point)
    
    print(f"✅ Telemetry removal complete!")
    print(f"🔒 Model metadata cleaned of tracking data")

def cmd_save(args):
    """Save modified virtual mount to new GGUF"""
    print(f"💾 Saving modifications: {args.mount_point} → {args.output_gguf}")
    
    # Load mount info
    try:
        with open('.gguf_cli_mounts.json', 'r') as f:
            mounts = json.load(f)
        
        if args.mount_point not in mounts:
            print(f"❌ No mount found at: {args.mount_point}")
            print(f"💡 Use 'mount' command first to create virtual mount")
            return
        
        extractor = GGUFExtractor()
        extractor.virtual_mounts[args.mount_point] = {
            'source_gguf': mounts[args.mount_point],
            'mount_point': args.mount_point
        }
        
        extractor.save_virtual_mount(args.mount_point, args.output_gguf)
        
        print(f"✅ Modified GGUF saved: {args.output_gguf}")
        print(f"🎉 Your fixed model is ready!")
        
    except FileNotFoundError:
        print(f"❌ No mount session found")
        print(f"💡 Use 'mount' command first to create virtual mount")

def cmd_cleanup(args):
    """Cleanup virtual mounts and temporary files"""
    print("🧹 Cleaning up virtual mounts...")
    
    extractor = GGUFExtractor()
    extractor.cleanup_virtual_mounts()
    
    # Remove CLI session file
    import os
    if os.path.exists('.gguf_cli_mounts.json'):
        os.remove('.gguf_cli_mounts.json')
    
    print("✅ Cleanup complete!")

def main():
    parser = argparse.ArgumentParser(
        description="🔧 GGUF Editor CLI - Fix broken tokenizers and edit GGUF files!",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  # Analyze a GGUF file
  python gguf_cli.py analyze model.gguf -v
  
  # Fix a broken tokenizer (like your endless <|end|> problem!)
  python gguf_cli.py mount broken_model.gguf /tmp/model
  python gguf_cli.py fix-tokenizer /tmp/model
  python gguf_cli.py save /tmp/model fixed_model.gguf
  
  # Strip telemetry from a model
  python gguf_cli.py mount model.gguf /tmp/model
  python gguf_cli.py strip-telemetry /tmp/model
  python gguf_cli.py save /tmp/model clean_model.gguf
  
  # Extract components for manual editing
  python gguf_cli.py extract model.gguf extracted/
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    parser_analyze = subparsers.add_parser('analyze', help='Analyze GGUF file structure')
    parser_analyze.add_argument('gguf_file', help='Path to GGUF file')
    parser_analyze.add_argument('-v', '--verbose', action='store_true', help='Show detailed information')
    parser_analyze.set_defaults(func=cmd_analyze)
    
    # Extract command
    parser_extract = subparsers.add_parser('extract', help='Extract GGUF to directory')
    parser_extract.add_argument('gguf_file', help='Path to GGUF file')
    parser_extract.add_argument('output_dir', help='Output directory')
    parser_extract.set_defaults(func=cmd_extract)
    
    # Mount command
    parser_mount = subparsers.add_parser('mount', help='Virtual mount GGUF file')
    parser_mount.add_argument('gguf_file', help='Path to GGUF file')
    parser_mount.add_argument('mount_point', help='Mount point directory')
    parser_mount.set_defaults(func=cmd_mount)
    
    # Fix tokenizer command
    parser_fix = subparsers.add_parser('fix-tokenizer', help='Fix broken tokenizer')
    parser_fix.add_argument('mount_point', help='Mounted GGUF directory')
    parser_fix.add_argument('--clean-tokenizer', help='Path to clean tokenizer file')
    parser_fix.set_defaults(func=cmd_fix_tokenizer)
    
    # Strip telemetry command
    parser_strip = subparsers.add_parser('strip-telemetry', help='Strip telemetry data')
    parser_strip.add_argument('mount_point', help='Mounted GGUF directory')
    parser_strip.set_defaults(func=cmd_strip_telemetry)
    
    # Save command
    parser_save = subparsers.add_parser('save', help='Save modified GGUF')
    parser_save.add_argument('mount_point', help='Mounted GGUF directory')
    parser_save.add_argument('output_gguf', help='Output GGUF file')
    parser_save.set_defaults(func=cmd_save)
    
    # Cleanup command
    parser_cleanup = subparsers.add_parser('cleanup', help='Cleanup virtual mounts')
    parser_cleanup.set_defaults(func=cmd_cleanup)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        args.func(args)
    except Exception as e:
        print(f"❌ Error: {e}")
        if args.command == 'analyze' and hasattr(args, 'verbose') and args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
