// コピーボタンのクリックイベントの処理
document.getElementById('copyButton').addEventListener('click', function () {
  // <pre> タグ内のテキストを取得
  var textToCopy = document.querySelector('pre').innerText;

  // テキストをクリップボードにコピー
  var dummy = document.createElement('textarea');
  document.body.appendChild(dummy);
  dummy.value = textToCopy;
  dummy.select();
  document.execCommand('copy');
  document.body.removeChild(dummy);

  var copyButton = document.getElementById('copyButton');
  copyButton.textContent = 'コピーしました';

  setTimeout(function () {
      copyButton.textContent = 'コピー';
  }, 500);
});

document.addEventListener("DOMContentLoaded", function () {
  const codeBlock = document.querySelector(".code-block");
  const codePre = codeBlock.querySelector("pre");
  const showFullCodeButton = document.querySelector(".show-full-code-button");

  let isFullCodeShown = false;

  showFullCodeButton.addEventListener("click", function () {
      if (isFullCodeShown) {
          codeBlock.classList.remove("pre-full-code");
          codePre.classList.remove("pre-full-code");
          isFullCodeShown = false;
          showFullCodeButton.textContent = "コードを全表示";
      } else {
          codeBlock.classList.add("pre-full-code");
          codePre.classList.add("pre-full-code");
          isFullCodeShown = true;
          showFullCodeButton.textContent = "コードを部分表示";
      }
  });
});
