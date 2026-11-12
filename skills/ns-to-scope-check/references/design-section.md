# Design section

Read first: `../ns-route/references/topic-tools.md`, `../ns-route/references/topic-learn-box.md`

Only for a real design choice. Show two designs when two are worth weighing, three when three are.

1. **Ground it.** Know the modules the change touches, who calls them, and why they are shaped as they are.
2. **Start from the caller.** For each design, write what the calling code will look like (the function call, the component usage, the request), then the types. Bodies stay unwritten.
3. **Make the designs differ in shape:** where the data lives, who owns the behavior, what the caller must know. Two variations of one idea are one design. Find candidates among the pattern this codebase already uses nearby, the simplest thing with no new structure, the shape the framework's docs recommend, and the shape you would choose if this requirement had existed from day one.
4. **Check each against this repo,** not from memory: the files and call sites it touches, what breaks, how it fails, how it behaves at ten times today's load, and how hard it is to delete.
5. **Prefer the deeper interface:** fewer things the caller must know, fewer ways to call it wrong.
6. **Screen for red flags.** Each is a reason to prefer the other design, or to say plainly why it is acceptable here:
   - the caller has to know the module's internal rules to use it correctly
   - the same knowledge lives in two places that must change together
   - a type needs an escape hatch to compile (`any`, a cast, an optional field that is always set)
   - a new abstraction with one caller
   - state shared between actors that could each own a copy
   - a change that looks right from one file is wrong for the repo
   - a special case for this ticket inside a general function
   - the design needs a lock, a retry, or a cache to be correct
7. **Pick,** with a one-line reason for each design ruled out, and end with a Learn box.

A library's or platform's real behavior you are unsure of: `context7` or `mattpocock-skills:research`. A question only trying can answer: `mattpocock-skills:prototype`, then throw the code away. Mark what stays unverified as *guess*.
