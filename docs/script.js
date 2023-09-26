document.addEventListener("DOMContentLoaded", function () {
  const codeBlock = document.querySelector(".code-block");
  const codePre = codeBlock.querySelector("pre");
  const copyButton = document.getElementById("copyButton"); // コピーボタンのIDを指定
  const showFullCodeButton = document.getElementById("ShowFullCodeButton"); // 全表示ボタンのIDを指定

  let isFullCodeShown = false;

  showFullCodeButton.addEventListener("click", function () {
      if (isFullCodeShown) {
          codeBlock.classList.remove("pre-full-code");
          isFullCodeShown = false;
          showFullCodeButton.textContent = "全表示";
      } else {
          codeBlock.classList.add("pre-full-code");
          isFullCodeShown = true;
          showFullCodeButton.textContent = "部分表示";
      }
  });

  copyButton.addEventListener("click", function () {
      const textArea = document.createElement("textarea");
      textArea.value = codePre.textContent;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand("copy");
      document.body.removeChild(textArea);
      alert("コードがクリップボードにコピーされました！");
  });
});
