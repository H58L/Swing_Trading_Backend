def calculate_BB(data):
            num_std_dev = 2
            # Calculate the middle band (20-day moving average by default)
            data['Middle Band'] = data['Close'].rolling(window=20).mean()
            
            # Calculate standard deviation
            data['Standard Deviation'] = data['Close'].rolling(window=20).std()
            
            # Calculate upper and lower bands
            data['Upper Band'] = data['Middle Band'] + (num_std_dev * data['Standard Deviation'])
            data['Lower Band'] = data['Middle Band'] - (num_std_dev * data['Standard Deviation'])
            
            # Drop rows with NaN values
            result = data[['Date','Close', 'Middle Band', 'Upper Band', 'Lower Band']].dropna().reset_index()
            return result