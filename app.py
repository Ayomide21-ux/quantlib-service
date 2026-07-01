from flask import Flask, request, jsonify
import QuantLib as ql

app = Flask(__name__)

@app.route('/price/european', methods=['POST'])
def price_option():
    data = request.json
    S = float(data['spot'])          # Underlying price
    K = float(data['strike'])        # Strike price
    r = float(data['rate'])          # Risk-free rate (e.g., 0.05 for 5%)
    sigma = float(data['volatility'])# Volatility (e.g., 0.20)
    T = float(data['maturity'])      # Time in years

    # QuantLib Black-Scholes for a European Call
    today = ql.Date().today()
    payoff = ql.PlainVanillaPayoff(ql.Option.Call, K)
    exercise = ql.EuropeanExercise(ql.Date().today() + ql.Period(int(T*365), ql.Days))
    option = ql.VanillaOption(payoff, exercise)

    # Set up the process
    spot_handle = ql.QuoteHandle(ql.SimpleQuote(S))
    rate_handle = ql.YieldTermStructureHandle(ql.FlatForward(today, r, ql.Actual360()))
    vol_handle = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), sigma, ql.Actual360()))
    process = ql.BlackScholesProcess(spot_handle, rate_handle, vol_handle)

    # Price it
    option.setPricingEngine(ql.AnalyticEuropeanEngine(process))
    price = option.NPV()

    return jsonify({
        "option_price": round(price, 4),
        "status": "QuantLib calculation successful on cloud"
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "QuantLib microservice live"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
