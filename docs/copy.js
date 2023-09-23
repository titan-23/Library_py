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

// 行数を表示する関数
function displayLineNumbers() {
  var codeBlock = document.querySelector('.code-block');
  var pre = codeBlock.querySelector('pre');
  var lineNumbers = codeBlock.querySelector('.line-numbers');

  // 改行をカウントして行数を表示
  var lineCount = pre.innerText.split('\n').length;
  var lines = '';
  for (var i = 1; i <= lineCount; i++) {
      lines += i + '<br>';
  }

  lineNumbers.innerHTML = lines;
}

// ページ読み込み時に行数を表示
window.addEventListener('load', displayLineNumbers);
