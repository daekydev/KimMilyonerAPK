using System;
using System.IO;
using Mono.Cecil;
using Mono.Cecil.Cil;

class Program
{
    static int Main(string[] args)
    {
        if (args.Length < 2)
        {
            Console.WriteLine("Usage: CecilPatcher <input_dll> <output_dll> [new_host]");
            Console.WriteLine("Example: CecilPatcher Assembly-CSharp.dll Assembly-CSharp.patched.dll http://10.0.2.2:5000");
            return 1;
        }

        string inputDll = args[0];
        string outputDll = args[1];
        string newHost = args.Length > 2 ? args[2].TrimEnd('/') : "http://10.0.2.2:5000";

        if (!File.Exists(inputDll))
        {
            Console.Error.WriteLine($"Error: Input file '{inputDll}' not found.");
            return 1;
        }

        Console.WriteLine($"Reading '{inputDll}'...");
        var assembly = AssemblyDefinition.ReadAssembly(inputDll);
        int patchCount = 0;

        foreach (var type in assembly.MainModule.Types)
        {
            patchCount += PatchType(type, newHost);
        }

        assembly.Write(outputDll);
        Console.WriteLine($"Successfully patched {patchCount} occurrences in '{outputDll}' with host '{newHost}'.");
        return 0;
    }

    static int PatchType(TypeDefinition type, string newHost)
    {
        int count = 0;
        foreach (var nested in type.NestedTypes)
        {
            count += PatchType(nested, newHost);
        }

        foreach (var field in type.Fields)
        {
            if (field.Constant is string s && s.Contains("api.wenetix.com"))
            {
                string replaced = s.Replace("http://api.wenetix.com", newHost);
                field.Constant = replaced;
                Console.WriteLine($"  [Field] {type.FullName}.{field.Name}: {s} -> {replaced}");
                count++;
            }
        }

        foreach (var method in type.Methods)
        {
            if (!method.HasBody) continue;
            foreach (var instr in method.Body.Instructions)
            {
                if (instr.OpCode == OpCodes.Ldstr && instr.Operand is string strVal)
                {
                    if (strVal.Contains("api.wenetix.com"))
                    {
                        string replaced = strVal.Replace("http://api.wenetix.com", newHost);
                        instr.Operand = replaced;
                        Console.WriteLine($"  [IL] {type.FullName}.{method.Name}: {strVal} -> {replaced}");
                        count++;
                    }
                }
            }
        }
        return count;
    }
}
