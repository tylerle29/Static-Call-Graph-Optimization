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

def main():
    g1 = load_call_graph("cg.json")
    g2 = load_call_graph("cg_og.json")

    differences = compare_call_graphs(g1, g2)
    with open("callgraph_diff.json", "w", encoding="utf-8") as f_json:
        json.dump(differences, f_json, indent=2)

    print_diff(differences)
    
if __name__ == "__main__":
    main()






    
