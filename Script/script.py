import json
import sys


import json

def load_call_graph(path):
    with open(path) as f:
        return json.load(f)

def method_signature(method):
    return f"{method['declaringClass']}::{method['name']}({','.join(method['parameterTypes'])}) -> {method['returnType']}"

def callsite_id(site):
    return f"line={site.get('line','?')},pc={site.get('pc','?')}"

def target_signature(target):
    return f"{target['declaringClass']}::{target['name']}({','.join(target['parameterTypes'])}) -> {target['returnType']}"

def compare_call_graphs(g1, g2):
    methods1 = {method_signature(m['method']): m for m in g1['reachableMethods']}
    methods2 = {method_signature(m['method']): m for m in g2['reachableMethods']}

    all_methods = sorted(set(methods1) | set(methods2))
    shared_methods = set(methods1) & set(methods2)

    diff = {
        "methods_only_in_graph1": sorted(set(methods1) - shared_methods),
        "methods_only_in_graph2": sorted(set(methods2) - shared_methods),
        "callsite_differences": {},
        "summary": {}
    }

    for method_sig in shared_methods:
        m1 = methods1[method_sig]
        m2 = methods2[method_sig]

        sites1 = {callsite_id(cs): cs for cs in m1.get("callSites", [])}
        sites2 = {callsite_id(cs): cs for cs in m2.get("callSites", [])}
        all_sites = set(sites1) | set(sites2)

        site_diffs = {}

        for sid in all_sites:
            cs1 = sites1.get(sid)
            cs2 = sites2.get(sid)

            targets1 = {target_signature(t) for t in cs1.get("targets", [])} if cs1 else set()
            targets2 = {target_signature(t) for t in cs2.get("targets", [])} if cs2 else set()

            if targets1 != targets2:
                site_diffs[sid] = {
                    "targets_only_in_graph1": sorted(targets1 - targets2),
                    "targets_only_in_graph2": sorted(targets2 - targets1),
                    "shared_targets": sorted(targets1 & targets2)
                }
        # --- Target similarity calculation ---
    total_targets_graph1 = set()
    total_targets_graph2 = set()
    shared_targets_total = set()

    for method_sig in shared_methods:
        m1 = methods1[method_sig]
        m2 = methods2[method_sig]

        sites1 = {callsite_id(cs): cs for cs in m1.get("callSites", [])}
        sites2 = {callsite_id(cs): cs for cs in m2.get("callSites", [])}

        all_sites = set(sites1) | set(sites2)

        for sid in all_sites:
            cs1 = sites1.get(sid)
            cs2 = sites2.get(sid)

            targets1 = {target_signature(t) for t in cs1.get("targets", [])} if cs1 else set()
            targets2 = {target_signature(t) for t in cs2.get("targets", [])} if cs2 else set()

            total_targets_graph1.update(targets1)
            total_targets_graph2.update(targets2)
            shared_targets_total.update(targets1 & targets2)

    all_unique_targets = total_targets_graph1 | total_targets_graph2
    target_similarity_ratio = len(shared_targets_total) / len(all_unique_targets) if all_unique_targets else 1.0

    
    if site_diffs:
        diff["callsite_differences"][method_sig] = site_diffs

    # Add summary
    diff["summary"] = {
        "total_methods_graph1": len(methods1),
        "total_methods_graph2": len(methods2),
        "shared_methods": len(shared_methods),
        "total_unique_methods": len(all_methods),
        "method_similarity_ratio": round(len(shared_methods) / len(all_methods), 4),
        "methods_only_in_graph1": len(diff["methods_only_in_graph1"]),
        "methods_only_in_graph2": len(diff["methods_only_in_graph2"]),
        "methods_with_target_differences": len(diff["callsite_differences"])
    }

    diff["summary"]["target_similarity_ratio"] = round(target_similarity_ratio, 4)
    diff["summary"]["total_unique_targets"] = len(all_unique_targets)
    diff["summary"]["shared_targets"] = len(shared_targets_total)


    return diff

def print_diff(diff):
    print("=== Method Differences ===")
    print("\nMethods only in Graph 1:")
    for m in diff["methods_only_in_graph1"]:
        print("  -", m)

    print("\nMethods only in Graph 2:")
    for m in diff["methods_only_in_graph2"]:
        print("  -", m)

    print("\n=== Target Differences in Shared Methods ===")
    for method, sites in diff["callsite_differences"].items():
        print(f"\nMethod: {method}")
        for site_id, site_diff in sites.items():
            print(f"  Call Site: {site_id}")
            if site_diff["targets_only_in_graph1"]:
                print("    Targets only in Graph 1:")
                for t in site_diff["targets_only_in_graph1"]:
                    print("      →", t)
            if site_diff["targets_only_in_graph2"]:
                print("    Targets only in Graph 2:")
                for t in site_diff["targets_only_in_graph2"]:
                    print("      →", t)

    print("\n=== Summary ===")
    for key, value in diff["summary"].items():
        print(f"  {key}: {value}")

def main():
    g1 = load_call_graph("cg_og.json")
    g2 = load_call_graph("cg.json")

    differences = compare_call_graphs(g1, g2)
    with open("callgraph_diff.json", "w", encoding="utf-8") as f_json:
        json.dump(differences, f_json, indent=2)

    print_diff(differences)

if __name__ == "__main__":
    main()


'''
import json

def load_call_graph(path):
    with open(path) as f:
        return json.load(f)

def method_signature(method):
    return f"{method['declaringClass']}::{method['name']}({','.join(method['parameterTypes'])}) -> {method['returnType']}"

def callsite_id(site):
    return f"line={site.get('line','?')},pc={site.get('pc','?')}"

def compare_call_graphs(g1, g2):
    methods1 = {method_signature(m['method']): m for m in g1['reachableMethods']}
    methods2 = {method_signature(m['method']): m for m in g2['reachableMethods']}

    all_method_keys = sorted(set(methods1) | set(methods2))

    diff = {
        "methods_only_in_graph1": [],
        "methods_only_in_graph2": [],
        "callsite_differences": {}
    }

    for key in all_method_keys:
        m1 = methods1.get(key)
        m2 = methods2.get(key)

        if not m1:
            diff["methods_only_in_graph2"].append(key)
            continue
        if not m2:
            diff["methods_only_in_graph1"].append(key)
            continue
        
    methods1_set = set(methods1.keys())
    methods2_set = set(methods2.keys())

    all_methods = methods1_set | methods2_set
    shared_methods = methods1_set & methods2_set

    method_similarity = len(shared_methods) / len(all_methods) if all_methods else 1.0
    print(f"Method similarity: {round(method_similarity * 100, 2)}%")

    diff["summary"] = {
        "total_methods_graph1": len(methods1_set),
        "total_methods_graph2": len(methods2_set),
        "shared_methods": len(shared_methods),
        "total_unique_methods": len(all_methods),
        "method_similarity_ratio": round(method_similarity, 4)
        }


        # Compare call sites
    sites1 = {callsite_id(cs): cs for cs in m1.get("callSites", [])}
    sites2 = {callsite_id(cs): cs for cs in m2.get("callSites", [])}
    all_sites = set(sites1) | set(sites2)

    site_diffs = {}

    for sid in all_sites:
        cs1 = sites1.get(sid)
        cs2 = sites2.get(sid)

        targets1 = {target_signature(t) for t in cs1.get("targets", [])} if cs1 else set()
        targets2 = {target_signature(t) for t in cs2.get("targets", [])} if cs2 else set()

        if targets1 != targets2:
            site_diffs[sid] = {
                "targets_only_in_graph1": sorted(targets1 - targets2),
                "targets_only_in_graph2": sorted(targets2 - targets1),
                "shared_targets": sorted(targets1 & targets2)
            }

    return diff

def target_signature(target):
    if not target:
        return "(missing)"
    return f"{target['declaringClass']}::{target['name']}({','.join(target['parameterTypes'])}) -> {target['returnType']}"

def print_clean_diff(diff):
    print("\n=== Methods Only in Graph 1 ===")
    for m in diff["methods_only_in_graph1"]:
        print("  -", m)

    print("\n=== Methods Only in Graph 2 ===")
    for m in diff["methods_only_in_graph2"]:
        print("  -", m)

    print("\n=== Call Site Differences ===")
    for method, sites in diff["callsite_differences"].items():
        print(f"\nMethod: {method}")
        for site_id, site_diff in sites.items():
            print(f"  Call Site: {site_id}")
            print("    - Graph 1:")
            if site_diff["graph1"]:
                for tgt in site_diff["graph1"].get("targets", []):
                    print("        →", format_target(tgt))
            else:
                print("        (missing)")
            print("    - Graph 2:")
            if site_diff["graph2"]:
                for tgt in site_diff["graph2"].get("targets", []):
                    print("        →", format_target(tgt))
            else:
                print("        (missing)")

def format_target(tgt):
    return f"{tgt['declaringClass']}::{tgt['name']}({','.join(tgt['parameterTypes'])}) -> {tgt['returnType']}"


def main():
    g1 = load_call_graph("cg_og.json")
    g2 = load_call_graph("cg.json")

    differences = compare_call_graphs(g1, g2)


    print_clean_diff(differences)


    with open("diff.json", "w") as f:
        json.dump(differences, f, indent=2)



if __name__ == "__main__":
    main()
'''

'''
def load_call_graph(file_path):
    with open(file_path) as f:
        return json.load(f)

def main():
    old_graph = load_call_graph("cg_og.json")
    new_graph = load_call_graph("cg.json")


    # Check structure and iterate through methods
    for method_entry in old_graph.get("reachableMethods", []):
        method = method_entry.get("method", {})
        print("Method:")
        print("  Name:", method.get("name"))
        print("  Declaring Class:", method.get("declaringClass"))
        print("  Return Type:", method.get("returnType"))
        print("  Parameters:", method.get("parameterTypes"))

        for site in method_entry.get("callSites", []):
            print("  Call Site:")
            print("    Line:", site.get("line"))
            print("    PC:", site.get("pc"))
            print("    Targets:")
            for target in site.get("targets", []):
                print("      -", target)

if __name__ == "__main__":
    main()
'''



'''
def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

old_graph = load_json("cg_og.json")
new_graph = load_json("cg.json")

print(old_graph["reachableMethods"]["method"])
'''

'''
def load_graph(path):
    with open(path) as f:
        return json.load(f)

def extract_func_name(call):
    if isinstance(call, dict):
        return call.get("name") or call.get("callee") or "<unknown>"
    return str(call)

def simplify(graph):
    simplified = {}
    for func, calls in graph.items():
        simplified[func] = [extract_func_name(c) for c in calls]
    return simplified

def compare(graph1, graph2):
    funcs1 = set(graph1)
    funcs2 = set(graph2)

    added_funcs = funcs2 - funcs1
    removed_funcs = funcs1 - funcs2
    common_funcs = funcs1 & funcs2

    changed_calls = []
    for func in common_funcs:
        calls1 = set(graph1[func])
        calls2 = set(graph2[func])
        if calls1 != calls2:
            changed_calls.append((func, calls1, calls2))

    return added_funcs, removed_funcs, changed_calls

def main(file1, file2):
    g1 = simplify(load_graph(file1))
    g2 = simplify(load_graph(file2))

    added, removed, changed = compare(g1, g2)

    with open("callgraph_diff.txt", "w") as out:
        out.write("=== Added Functions ===\n")
        for f in sorted(added):
            out.write(f" + {f}\n")

        out.write("\n=== Removed Functions ===\n")
        for f in sorted(removed):
            out.write(f" - {f}\n")

        out.write("\n=== Changed Call Targets ===\n")
        for func, old, new in changed:
            out.write(f" * {func}\n")
            out.write(f"     Old: {sorted(old)}\n")
            out.write(f"     New: {sorted(new)}\n")

    print("✅ Diff written to callgraph_diff.txt")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python compare_call_graphs.py old.json new.json")
    else:
        main(sys.argv[1], sys.argv[2])
'''

'''
from deepdiff import DeepDiff

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

old_graph = load_json("cg_og.json")
new_graph = load_json("cg.json")

diff = DeepDiff(old_graph, new_graph, verbose_level=2)

with open("diff_output.txt", "w") as out_file:
    if diff:
        out_file.write("=== Differences Detected ===\n")
        out_file.write(diff.pretty())  # Pretty format
    else:
        out_file.write("✅ No differences found.\n")

        */
'''
#if diff:
#    print("=== Differences Detected ===")
#    print(diff.pretty())
#else:
#    print("✅ No differences found")

#f = open("myfile.txt", "w")
#with open("demofile.txt", "w") as f:
#    f.write(diff)




def main():
    g1 = load_call_graph("cg.json")
    g2 = load_call_graph("cg_og.json")

    differences = compare_call_graphs(g1, g2)
    with open("callgraph_diff.json", "w", encoding="utf-8") as f_json:
        json.dump(differences, f_json, indent=2)

    print_diff(differences)
    
if __name__ == "__main__":
    main()






    