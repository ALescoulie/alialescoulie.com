
## A FOSS online graphing calculator inspired by Desmos

### [Project Source](https://github.com/ALescoulie/faraday)

In high school I loved, [Desmos](https://desmos.com).
It was great for visualizing problems in Trigonometry, made some nice looking graphs.
I loved how it let me dynamically view and transform mathematical expressions and learn a ton about modeling real world problems.
I found though that as I went further into my education in math and science, and learning to code, Desmos felt increasingly limited.
I found that it was incontinent for working with arrays and vectors since it doesn't have indexing.
I also found that it was not free open-source software, and I decided I'd try and make my own version that addressed what I found limited desmos, and that was fully open-source and ran client-side.
I named the project after Michael Faraday because of his use of visualizations to illustrate concepts in electromagnetism.

## Project Summary

Faraday was a mix of wanting a piece of software to exist, and wanting to build my own skills while doing so.
In that vein I ended up using three technologies relatively that were mostly new to me: TypeScript, React, and Haskell.
It might have been a bad idea to use three new technologies for this project, but I since I only needed each technology for one step I decided it was fine.
I used Haskell to parse the math syntax, inputted in a domain specific language I named mentat (I've been reading a lot of Dune), into executable JavaScript.
This project made me fall in love with Haskell and functional programming in general, and was a great language for transpiring code.
I then compiled the Haskell into web assembly so that I could import it into my TypeScript. 
The rest of Faraday is build in TypeScript and React, or at time of writing will be.

