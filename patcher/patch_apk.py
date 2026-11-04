#!/usr/bin/env python3
"""
Kim Bir Milyon İster APK / DLL Patcher
Replaces http://api.wenetix.com with the custom server URL (e.g. http://10.0.2.2:5000 or http://192.168.1.X:5000)
"""

import sys
import os
import shutil
import zipfile
import subprocess
import tempfile
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CECIL_PATCHER_DLL = os.path.join(SCRIPT_DIR, "CecilPatcher", "bin", "Debug", "net8.0", "CecilPatcher.dll")


def patch_dll(input_dll_path, output_dll_path, new_host):
    """Patches Assembly-CSharp.dll using CecilPatcher."""
    if not os.path.exists(CECIL_PATCHER_DLL):
        # Build CecilPatcher if not built yet
        subprocess.run(["dotnet", "build", os.path.join(SCRIPT_DIR, "CecilPatcher")], check=True)

    cmd = ["dotnet", CECIL_PATCHER_DLL, input_dll_path, output_dll_path, new_host]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("CecilPatcher error:\n", res.stderr)
        raise RuntimeError(f"CecilPatcher failed with exit code {res.returncode}")
    print(res.stdout)


def patch_apk(input_apk_path, output_apk_path, new_host):
    """Extracts Assembly-CSharp.dll from input APK, patches it, and repacks into output APK."""
    print(f"[*] Patching APK: {input_apk_path}")
    print(f"[*] Target Server URL: {new_host}")

    with tempfile.TemporaryDirectory() as temp_dir:
        dll_name = "assets/bin/Data/Managed/Assembly-CSharp.dll"
        extracted_dll = os.path.join(temp_dir, "Assembly-CSharp.dll")
        patched_dll = os.path.join(temp_dir, "Assembly-CSharp.patched.dll")

        # 1. Extract Assembly-CSharp.dll
        found = False
        with zipfile.ZipFile(input_apk_path, 'r') as zin:
            for item in zin.infolist():
                if item.filename == dll_name:
                    with open(extracted_dll, 'wb') as f:
                        f.write(zin.read(item.filename))
                    found = True
                    break

        if not found:
            raise FileNotFoundError(f"Could not find {dll_name} in {input_apk_path}")

        # 2. Patch the extracted DLL
        patch_dll(extracted_dll, patched_dll, new_host)

        # 3. Create new APK with patched DLL (skipping old signature files)
        print("[*] Rebuilding APK package...")
        with zipfile.ZipFile(input_apk_path, 'r') as zin, zipfile.ZipFile(output_apk_path, 'w') as zout:
            for item in zin.infolist():
                # Skip signature files so it can be re-signed cleanly
                if item.filename.startswith("META-INF/") and (
                    item.filename.endswith(".SF") or item.filename.endswith(".RSA") or item.filename.endswith(".DSA")
                ):
                    continue
                if item.filename == dll_name:
                    with open(patched_dll, 'rb') as f:
                        data = f.read()
                    zout.writestr(item, data)
                else:
                    try:
                        data = zin.read(item.filename)
                        zout.writestr(item, data)
                    except Exception as e:
                        # For unreadable/corrupted files in damaged source APK, copy raw data if available
                        print(f"[-] Warning: Failed reading {item.filename}: {e}")

        # 4. Sign APK if keystore available or generate debug keystore
        keystore_path = os.path.join(temp_dir, "debug.keystore")
        generate_keystore_and_sign(output_apk_path, keystore_path)

    print(f"[+] Done! Patched APK created at: {output_apk_path}")


def generate_keystore_and_sign(apk_path, keystore_path):
    """Generates a temporary debug keystore and signs the APK with jarsigner."""
    print("[*] Signing APK with debug certificate...")
    if shutil.which("keytool") and shutil.which("jarsigner"):
        # Generate debug key
        keytool_cmd = [
            "keytool", "-genkey", "-v",
            "-keystore", keystore_path,
            "-storepass", "android",
            "-alias", "androiddebugkey",
            "-keypass", "android",
            "-keyalg", "RSA",
            "-keysize", "2048",
            "-validity", "10000",
            "-dname", "CN=Android Debug,O=Android,C=US"
        ]
        subprocess.run(keytool_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        jarsigner_cmd = [
            "jarsigner",
            "-sigalg", "SHA1withRSA",
            "-digestalg", "SHA1",
            "-keystore", keystore_path,
            "-storepass", "android",
            "-keypass", "android",
            apk_path,
            "androiddebugkey"
        ]
        subprocess.run(jarsigner_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print("[+] APK successfully signed.")
    else:
        print("[-] Notice: jarsigner or keytool not found in PATH. Skipping signature.")


def main():
    parser = argparse.ArgumentParser(description="Patch Kim Bir Milyon İster APK or DLL with custom server URL.")
    parser.add_argument("--apk", help="Path to input APK file")
    parser.add_argument("--dll", help="Path to input Assembly-CSharp.dll file directly")
    parser.add_argument("--output", "-o", required=True, help="Path to output APK or DLL file")
    parser.add_argument("--host", default="http://10.0.2.2:5000", help="New server base URL (e.g. http://10.0.2.2:5000 or http://192.168.1.50:5000)")

    args = parser.parse_args()

    if args.apk:
        patch_apk(args.apk, args.output, args.host)
    elif args.dll:
        patch_dll(args.dll, args.output, args.host)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
