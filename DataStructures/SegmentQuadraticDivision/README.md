最終更新：2022/12/09  
・readmeを整備しました  
更新予定  
・  

_____
# [LazyQuadraticDivision](https://github.com/titanium-22/Library/blob/main/QuadraticDivision/LazyQuadraticDivision.py)
区間の総積取得・区間への作用適用クエリをそれぞれ時間計算量 $\mathcal{O}(\sqrt{N})$ で処理できるデータ構造です。計算量が $\mathcal{O}(\sqrt{N})$ になった遅延セグ木ともみなせます。  
定数倍が軽いのでそこまで遅くはないはずです。  
以下、計算量を明示していないものは計算量 $\mathcal{O}(\sqrt{N})$ とします。  


### ```qd = LazyQuadraticDivision(n_or_a: Iterable[T], op: Callable[[T, T], T], mapping: Callable[[F, T], T], composition: Callable[F, F], F], e: T)```
列 $\mathsf{a}$ から $\mathsf{LazyQuadraticDivision}$ を構築します。その他引数は遅延セグ木のアレです。
$\mathsf{n}$ の型を $\mathsf{int}$ にすると、 $\mathsf{n}$ 個の $\mathsf{e}$ からなる配列で $\mathsf{LazyQuadraticDivision}$ を構築します。  
計算量 $\mathcal{O}(N)$ です。

### ```qd.apply(l: int, r: int, f: F) -> None```
区間 $\mathsf{\left[l, r\right)}$ に $\mathsf{f}$ を適用します。

### ```qd.all_apply(f: F) -> None```
区間 $\mathsf{\left[0, N\right)}$ に $\mathsf{f}$ を適用します。

### ```qd[k] -> T```
$\mathsf{k}$ 番目の値を返します。

### ```qd[k] = key```
$\mathsf{k}$ 番目の値を $\mathsf{key}$ に変更します。

### ```qd.prod(l: int, r: int) -> T```
区間 $\mathsf{\left[l, r\right)}$ に $\mathsf{op}$ を適用した総積を返します。

### ```qd.all_prod() -> T```
区間 $\mathsf{\left[0, N\right)}$ に $\mathsf{op}$ を適用した総積を返します。


_____
# [QuadraticDivision](https://github.com/titanium-22/Library/blob/main/QuadraticDivision/QuadraticDivision.py)

区間の総積取得クエリを時間計算量 $\mathcal{O}(\sqrt{N})$ で処理できるデータ構造です。計算量が $\mathcal{O}(\sqrt{N})$ になった普通のセグ木ともみなせます。  
遅延評価の処理を必要としないため、[LazyQuadraticDivision](https://github.com/titanium-22/Library/blob/main/QuadraticDivision/QuadraticDivision.py)より定数倍が軽いです。  
以下、計算量を明示していないものは計算量 $\mathcal{O}(\sqrt{N})$ とします。  


### ```qd = QuadraticDivision(n_or_a: Iterable[T], op: Callable[[T, T], T], e: T)```
列 $\mathsf{a}$ から $\mathsf{QuadraticDivision}$ を構築します。その他引数はセグ木のアレです。
$\mathsf{n}$ の型を $\mathsf{int}$ にすると、 $\mathsf{n}$ 個の $\mathsf{e}$ からなる配列で $\mathsf{QuadraticDivision}$ を構築します。  

計算量 $\mathcal{O}(N)$ です。

### ```その他メソッド```
[LazyQuadraticDivision](https://github.com/titanium-22/Library/blob/main/QuadraticDivision/QuadraticDivision.py)から```apply(), all_apply```を除いたメソッドが使用可能です。
