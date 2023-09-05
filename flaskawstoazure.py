import pandas as pd
from flask import Flask

app = Flask(__name__)
df_aws = pd.read_csv("AWSVMr.csv")
df_azure = pd.read_csv("AZUREVMr.csv")

@app.route('/vm_tier_aws/<memory>/<core>')
def vm_tier_aws(memory=None, core=None):
    aws_memory = int(memory)
    aws_core = int(core)

 
    azure_result = df_azure[(df_azure['Memory'] == aws_memory) & (df_azure['Core'] == aws_core)]

    if not azure_result.empty:
        azure_tiers = azure_result['Tier'].values.tolist()
        return ({"Matching_Azure_Tiers": azure_tiers})
    else:
        
        min_diff_idx = ((df_azure['Memory'] - aws_memory).abs() + (df_azure['Core'] - aws_core).abs()).idxmin()
        config = df_azure.loc[min_diff_idx]
        tiers_config = df_azure[(df_azure['Memory'] == config['Memory']) & (df_azure['Core'] == config['Core'])]['Tier'].values.tolist()
        return f"Available configuration in AZURE: Memory:{config['Memory']}, Core:{config['Core']}, Tiers:{config['Tier']},{','.join(tiers_config)}"
    
if __name__ == '__main__':
    app.run()

   