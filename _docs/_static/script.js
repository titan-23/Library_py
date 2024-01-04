
document.addEventListener("DOMContentLoaded", function () {
  const codeBlock = document.querySelector(".code-block"); // .code-block クラスを持つ要素を選択
  
  if (codeBlock) { // 要素が存在するか確認
      const copyButton = document.getElementById("copyButton");
      const showFullCodeButton = document.getElementById("ShowFullCodeButton");
      const toggleCodeButton = document.getElementById("toggleCodeButton");
      const codeContainer1 = document.getElementById("codeContainer1");
      const codeContainer2 = document.getElementById("codeContainer2");

      let isFullCodeShown = false;
      let isAlternateCodeShown = false;
      
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
          let codeToCopy = "";
          if (isAlternateCodeShown) {
              codeToCopy = codeContainer2.querySelector("pre").textContent;
          } else {
              codeToCopy = codeContainer1.querySelector("pre").textContent;
          }

          const textArea = document.createElement("textarea");
          textArea.value = codeToCopy;
          document.body.appendChild(textArea);
          textArea.select();
          document.execCommand("copy");
          document.body.removeChild(textArea);

          // ボタンの内容を変更
          copyButton.textContent = "コピーしました";

          // 1秒後にボタンの内容を元に戻す
          setTimeout(function () {
              copyButton.textContent = "コピー";
          }, 1000);
      });

      toggleCodeButton.addEventListener("click", function () {
          if (isAlternateCodeShown) {
              codeContainer1.style.display = "block";
              codeContainer2.style.display = "none";
              toggleCodeButton.textContent = "展開";
          } else {
              codeContainer1.style.display = "none";
              codeContainer2.style.display = "block";
              toggleCodeButton.textContent = "縮小";
          }
          isAlternateCodeShown = !isAlternateCodeShown;
      });

  }
});