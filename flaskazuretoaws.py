import pandas as pd
from flask import Flask

app = Flask(__name__)
df_azure = pd.read_csv("AZUREVMr.csv")
df_aws = pd.read_csv("AWSVMr.csv")

@app.route('/vm_tier_azure/<memory>/<core>')
def vm_tier_azure(memory=None, core=None):
    azure_memory = int(memory)
    azure_core = int(core)

 
    aws_result = df_aws[(df_aws['Memory'] == azure_memory) & (df_aws['Core'] == azure_core)]

    if not aws_result.empty:
        aws_tiers = aws_result['Tier'].values.tolist()
        return ({"Matching_AWS_Tiers": aws_tiers})
    else:
        
        min_diff_idx = ((df_aws['Memory'] - azure_memory).abs() + (df_aws['Core'] - azure_core).abs()).idxmin()
        config = df_aws.loc[min_diff_idx]
        tiers_config = df_aws[(df_aws['Memory'] == config['Memory']) & (df_aws['Core'] == config['Core'])]['Tier'].values.tolist()
        return f"Available configuration in AWS: Memory:{config['Memory']}, Core:{config['Core']}, Tiers:{config['Tier']},{','.join(tiers_config)}"
    
if __name__ == '__main__':
    app.run()

