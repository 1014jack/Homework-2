# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

> Solution

(tokenB -> tokenA) : (5, 5.655321988655323)

(tokenA -> tokenC) : (5.655321988655323, 2.372138936383089)

(tokenC -> tokenE) : (2.372138936383089, 1.530137136963617)

(tokenE -> tokenD) : (1.530137136963617, 3.4507414486197083)

(tokenD -> tokenC) : (3.4507414486197083, 6.684525579572587)

(tokenC -> tokenB) : (6.684525579572587, 22.497221806974142)

path: tokenB->tokenA->tokenC->tokenE->tokenD->tokenC->tokenB, tokenB balance=22.497221806974142


## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

> Solution

Slippage in an Automated Market Maker (AMM) context refers to the difference between the expected price of a token swap and the actual price achieved when the trade is executed. This difference arises because AMM liquidity pools rely on supply and demand to determine token prices.

uniswapV2 revert transection when expected amountOut < amountOutMin
```
amounts = UniswapV2Library.getAmountsOut(factory, amountIn, path);
require(amounts[amounts.length - 1] >= amountOutMin, 'UniswapV2Router: INSUFFICIENT_OUTPUT_AMOUNT');
```


## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

> Solution

Some LP token is burned to ensure no one has all the LP tokens, preventing "inflation attack".

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

> Solution

This formula provide incentivizes provider to increase the supply of token0 and token1 without changing the ratio of token0 and token1.

And prevent someone from getting much more value of liquidity than he deposit.

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

> Solution

Sandwich attack is someone front-run my transection, reduce the expact value to my lowest slippage range.

After my transection done, they swap their transection to gain interest.

