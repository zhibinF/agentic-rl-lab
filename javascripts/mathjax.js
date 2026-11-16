// Loaded before MathJax: only process the wrappers emitted by Arithmatex.
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  },
  startup: {
    typeset: false,
    ready() {
      MathJax.startup.defaultReady();
      // Wait for the engine, including when the CDN loads slowly. Serialize
      // navigation updates so MathJax never typesets two documents at once.
      MathJax.startup.promise.then(() => {
        let pending = Promise.resolve();
        let previousArticle;
        document$.subscribe(() => {
          pending = pending.then(() => {
            const article = document.querySelector("article");
            if (article === previousArticle) return;
            previousArticle = article;
            MathJax.typesetClear();
            MathJax.texReset();
            return MathJax.typesetPromise();
          });
        });
      });
    }
  }
};
