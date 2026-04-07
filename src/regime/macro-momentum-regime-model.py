# import yfinance as yf
# import pandas as pd
# import smtplib
# from email.mime.text import MIMEText
# from datetime import datetime


# # -----------------------------------------------------
# # FX PAIRS + WEIGHTS
# # -----------------------------------------------------

# pairs = {
#     "AUDJPY=X": "Global risk appetite",
#     "USDJPY=X": "U.S.-Japan liquidity & yields",
#     "EURCHF=X": "European geopolitical stress",
#     "AUDCAD=X": "Metals/China vs Oil/U.S.",
#     "NZDJPY=X": "Secondary (ag) risk gauge",
#     "USDMXN=X": "EM risk & carry stress"
# }

# PAIR_WEIGHTS = {
#     "AUDJPY=X": 0.30,
#     "USDJPY=X": 0.20,
#     "EURCHF=X": 0.15,
#     "NZDJPY=X": 0.15,
#     "AUDCAD=X": 0.10,
#     "USDMXN=X": 0.10
# }



# # -----------------------------------------------------
# # Z-SCORE CALCULATOR
# # -----------------------------------------------------
# # ---------- REPLACEMENT: zscore on returns (safe for DF/Series) ----------
# def zscore_series_returns(series, window=60, min_periods=30):
#     """
#     Compute today's Z-score based on percent returns for a Series (price series).
#     Returns 0 if not enough data or std == 0.
#     """
#     # If DataFrame slipped through, pick Close or first column
#     if isinstance(series, pd.DataFrame):
#         if "Close" in series:
#             series = series["Close"]
#         else:
#             series = series.iloc[:, 0]

#     # compute percent returns (as percentages, not fraction)
#     returns = series.pct_change().dropna() * 100.0

#     if len(returns) < min_periods:
#         return 0.0

#     windowed = returns[-window:]
#     mu = windowed.mean()
#     sigma = windowed.std()

#     if sigma == 0 or pd.isna(sigma):
#         return 0.0

#     # today's return is the last element of returns
#     today_ret = returns.iloc[-1]

#     return (today_ret - mu) / sigma




# # -----------------------------------------------------
# # FX DOWNLOAD + SCORING
# # -----------------------------------------------------
# def score_fx_change(pct):
#     if pct > 1.0:
#         return 2
#     elif pct > 0.25:
#         return 1
#     elif pct < -1.0:
#         return -2
#     elif pct < -0.25:
#         return -1
#     else:
#         return 0


# def download_fx_data():
#     data = yf.download(list(pairs.keys()), start="2025-10-01")["Close"]
#     return data.dropna()


# def generate_signals(df):
#     if len(df) < 2:
#         return None, None, None, None

#     today = df.iloc[-1]
#     yesterday = df.iloc[-2]

#     pct_changes = (today - yesterday) / yesterday * 100
#     scores = pct_changes.apply(score_fx_change)
#     weighted_scores = scores * pd.Series(PAIR_WEIGHTS)

#     return today, yesterday, pct_changes, weighted_scores



# # -----------------------------------------------------
# # MACRO DOWNLOAD + SCORING
# # -----------------------------------------------------
# def get_macro_today_yesterday():
#     symbols = {
#         "VIX": "^VIX",
#         "SPX": "^GSPC",
#         "UST10": "^TNX",
#         "WTI": "CL=F"
#     }

#     macro = {}

#     for name, symbol in symbols.items():
#         df = yf.download(symbol, period="7d")["Close"].dropna()
#         macro[name] = {
#             "today": df.iloc[-1].item(),
#             "yesterday": df.iloc[-2].item()
#         }

#     return macro


# def get_macro_history():
#     symbols = {
#         "VIX": "^VIX",
#         "SPX": "^GSPC",
#         "UST10": "^TNX",
#         "WTI": "CL=F"
#     }

#     hist = {}
#     for name, symbol in symbols.items():
#         df = yf.download(symbol, period="6mo")["Close"].dropna()
#         hist[name] = df

#     return hist



# # -----------------------------------------------------
# # MACRO SCORING
# # -----------------------------------------------------
# def score_vix(vix):
#     if vix < 14:
#         return 1
#     elif vix > 20:
#         return -1
#     else:
#         return 0


# def score_spx(today, yesterday):
#     pct = (today - yesterday) / yesterday * 100
#     if pct > 0.75:
#         return 1
#     elif pct < -0.75:
#         return -1
#     return 0


# def score_yields(ust10):
#     if ust10 > 4.0:
#         return 1
#     elif ust10 < 3.0:
#         return -1
#     return 0


# def score_oil(today, yesterday):
#     pct = (today - yesterday) / yesterday * 100
#     if pct > 1.0:
#         return 1
#     elif pct < -1.0:
#         return -1
#     return 0


# def build_macro_sentiment(macro):
#     vix_s = score_vix(macro["VIX"]["today"])
#     spx_s = score_spx(macro["SPX"]["today"], macro["SPX"]["yesterday"])
#     ust_s = score_yields(macro["UST10"]["today"])
#     wti_s = score_oil(macro["WTI"]["today"], macro["WTI"]["yesterday"])

#     total_macro = vix_s + spx_s + ust_s + wti_s

#     return {
#         "VIX": vix_s,
#         "SPX": spx_s,
#         "UST10": ust_s,
#         "WTI": wti_s,
#         "TotalMacro": total_macro
#     }



# # -----------------------------------------------------
# # REPORT GENERATION
# # -----------------------------------------------------
# def build_report(today, yesterday, pct, weighted_scores, macro_scores, fx_zscores, macro_zscores):
#     report = []
#     report.append("📈 DAILY FX MACRO REPORT")
#     report.append("Date: " + datetime.now().strftime("%Y-%m-%d"))
#     report.append("\n----------------------------------\n")

#     # FX section
#     for pair in pairs:
#         raw_score = score_fx_change(pct[pair])
#         report.append(
#             f"{pair}: {pairs[pair]}\n"
#             f"  Today: {today[pair]: .4f}\n"
#             f"  Yesterday: {yesterday[pair]: .4f}\n"
#             f"  Change: {pct[pair]: .2f}%\n"
#             f"  Score: {raw_score} (Weighted: {weighted_scores[pair]: .2f})\n"
#             f"  Z-score: {fx_zscores[pair]: .2f}\n"
#         )

#     total_fx_mri = weighted_scores.sum()

#     # Macro section
#     report.append("\n----------------------------------\n")
#     report.append(
#         f"VIX Score: {macro_scores['VIX']}\n"
#         f"SPX Score: {macro_scores['SPX']}\n"
#         f"Yields: {macro_scores['UST10']}\n"
#         f"Oil (WTI): {macro_scores['WTI']}\n"
#         f"Macro Total: {macro_scores['TotalMacro']}\n"
#     )

#     # Compute Z-score aggregates
#     fx_z_avg = sum(fx_zscores.values()) / len(fx_zscores)
#     macro_z_avg = (
#         macro_zscores["VIX"] +
#         macro_zscores["SPX"] +
#         macro_zscores["UST10"] +
#         macro_zscores["WTI"]
#     ) / 4

#     # Hybrid score
#     hybrid = (
#         total_fx_mri
#         + 0.5 * macro_scores["TotalMacro"]
#         + 0.3 * fx_z_avg
#         + 0.2 * macro_z_avg
#     )

#     # Final sentiment classification
#     sentiment = (
#         "STRONG RISK-ON" if hybrid >= 1.0 else
#         "MILD RISK-ON"   if hybrid >= 0.25 else
#         "NEUTRAL"        if hybrid > -0.25 else
#         "MILD RISK-OFF"  if hybrid > -1.0 else
#         "STRONG RISK-OFF"
#     )

#     report.append("\n--------------------------------")
#     report.append(f"FX MRI: {total_fx_mri:.2f}")
#     report.append(f"Macro Score: {macro_scores['TotalMacro']:.2f}")
#     report.append(f"FX Z Avg: {fx_z_avg:.2f}")
#     report.append(f"Macro Z Avg: {macro_z_avg:.2f}")
#     report.append(f"\nHYBRID SCORE: {hybrid:.2f}")
#     report.append(f"FINAL SENTIMENT: **{sentiment}**")
#     report.append("--------------------------------")

#     return "\n".join(report)



# # -----------------------------------------------------
# # MAIN
# # -----------------------------------------------------
# df = download_fx_data()
# today, yesterday, pct, weighted_scores = generate_signals(df)

# if today is None:
#     print("Not enough FX data to run.")
# else:
#     # FX Z-scores
#     fx_zscores = {pair: zscore_series_returns(df[pair], window=60, min_periods=30) for pair in df.columns}

#     # Macro
#     macro = get_macro_today_yesterday()
#     macro_scores = build_macro_sentiment(macro)

#     # Macro Z-scores (long history)
#     macro_hist = get_macro_history()
#     macro_zscores = {
#         name: zscore_series_returns(macro_hist[name], window=60, min_periods=30)
#         for name in macro_hist
#     }

#     report = build_report(
#         today, yesterday, pct, weighted_scores,
#         macro_scores, fx_zscores, macro_zscores
#     )

#     print(report)
