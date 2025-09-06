# Static Call Graph Optimization

This tool tries to create dynamic ground truths with multiple entry points. This is an expansion on a project by Dr. Helm and his lab; however, it varies greatly in methodology.
<img width="1972" height="776" alt="image" src="https://github.com/user-attachments/assets/d96e6119-3919-497e-8a51-67fbcb3ab5c9" />

Download the tar file if you want to recreate this experiment. Results for test_cases created through fuzzing and results are shown in the GIT Project.

Prerequisites:
-Use a Linux terminal
-Get Docker and Just
-Have Python
-Java 1.8+ and a JDK
Implementing a new Fuzzer
1) Define a *Base Corpus* (set of inputs). The scripts 
`/projects/<project>/prepare_base_corpus.sh` are responsible for 
aggregating these base corpora.
- If project needs multiple inputs to work, split into folders of fuzzed 
inputs and fixed inputs
- If you want to fuzz both of them, add delimiters and make seeds into 
one folder.
2) Define dependencies for project. The scripts are at 
`/java-corpora/xcorpus` are responsible for aggregating them.
3) Define manual extensions to the Base Corpus to form the *Seed Corpus*. 
The scripts `/projects/<project>/prepare_seed_corpus.sh` are responsible 
for aggregating these seed corpora and are executed after 
`prepare_base_corpus.sh` has been called.
- Some target programs may need extra work done on the files to start
the fuzzing process. You can add a python script here. See 
`/projects/xerces/prepare_seed_corpus.sh’ for example.
4) Find a suitable dictionary (`dict.txt`) to guide the fuzzing process. 
`/projects/<project>/prepare_dictionary.sh` copies those files to their 
destination for each project.
- Use AFL++ dictionaries.
- If multiple inputs, you might need to combine dictionaries.
5) Pick an entrypoint to your program and wrap it inside a main method. 
Examples can be found in `/projects/<project>/src/Entrypoint.java`.
- ChatGTP can create a skeleton for entry points. You need to edit that
skeleton manually based on needs.
6) Create a [Fuzzer implementation]
(https://github.com/CodeIntelligenceTesting/jazzer/tree/main/examples/
src/main/java/com/example) for your project. See 
`/projects/<project>/src/<project>Fuzzer.java`.
- Fuzzing harnesses are usually only able to take one input. Work 
arounds like delimiters and file paths can be used to get around this.
7) Edit environment folder `/projects/<project>/.env’. These folders may 
need to be moved up to the project level directory.
8) Provide the sources for the new project. This is currently done via the 
XCorpus Docker image (`/java-corpora/xcorpus`) and limited to projects 
contained in the XCorpus benchmark.
- This can be quickly edited to include other benchmarks.
9) Edit the dynamic call graph generator based on your own needs. If your 
entry point is designed well, this should work on its own.



10) For generation of dynamic call graphs, run in an Ubuntu shell at 
`/projects/<project>’
- just clean
- just do_fuzzing_seed
- just dynamic_callgraph_fuzzing_seed
11) To edit aspects of fuzzing like time, you can look at the 
‘/projects/JustFile’ or do it in line.
