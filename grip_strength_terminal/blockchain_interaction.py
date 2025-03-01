import asyncio
import base64
from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import List
import os
from chained_accounts import ChainedAccount
from telliot_core.apps.core import RPCEndpoint
from telliot_core.utils.response import error_status
from telliot_core.utils.response import ResponseStatus
from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.core.coins import Coin
from chained_accounts import ChainedAccount

from telliot_feeds.datafeed import DataFeed
from telliot_feeds.feeds import CATALOG_FEEDS
from telliot_feeds.queries.grip_dyno_challenge_query import EthDenverTester
from telliot_feeds.reporters.layer.client import LCDClient
from telliot_feeds.reporters.layer.msg_submit_value import MsgSubmitValue
from telliot_feeds.reporters.layer.msg_tip import MsgTip
from telliot_feeds.reporters.layer.raw_key import RawKey
from telliot_feeds.datasource import DataSource
from telliot_feeds.utils.log import get_logger
from telliot_feeds.utils.query_search_utils import feed_from_catalog_feeds
from telliot_feeds.utils.reporter_utils import is_online
from grip_strength_terminal.loading_animation import LoadingSpiral

logger = get_logger(__name__)
    
def clear_terminal():
    # Clear screen command for different operating systems
    os.system('cls' if os.name == 'nt' else 'clear')

class GripStrengthData:
    def __init__(self, data_set, right_hand, left_hand, x_handle, github_username, hours_of_sleep):
        self.data_set = data_set
        # Convert grip strength values to floats and add 18 decimal places
        self.right_hand = int(float(right_hand) * (10 ** 18))  # Convert to Wei-like precision
        self.left_hand = int(float(left_hand) * (10 ** 18))    # Convert to Wei-like precision
        self.x_handle = x_handle
        self.github_username = github_username
        self.hours_of_sleep = hours_of_sleep

class GripStrengthDataSource(DataSource[Any]):
    def __init__(self, grip_data: GripStrengthData):
        self.grip_data = grip_data

    async def fetch_new_datapoint(self):
        return self.grip_data

class GripStrengthReporter:
    def __init__(
        self,
        grip_data: List[GripStrengthData],
        endpoint: RPCEndpoint,
        account: ChainedAccount,
        query_tag: Optional[str] = None,
        datafeed: Optional[DataFeed[Any]] = None,
        ignore_tbr: bool = False,
        gas: str = "auto",
    ) -> None:
        self.account = account
        self.primary_endpoint = endpoint
        self.backup_endpoint = RPCEndpoint(
            url=os.getenv('TELLOR_RPC_URL_BACKUP', 'http://tellorlayer.com:1317'),
            network="layertest-3"
        )
        self.gas = gas
        self.current_endpoint = self.primary_endpoint
        self.client = LCDClient(url=self.current_endpoint.url, chain_id=self.current_endpoint.network)

    async def switch_to_backup(self):
        """Switch to backup endpoint and create new client"""
        self.current_endpoint = self.backup_endpoint
        self.client = LCDClient(url=self.backup_endpoint.url, chain_id=self.backup_endpoint.network)
        print("\nSwitching to backup RPC endpoint...")

    async def report_grip_query(self, datafeed: DataFeed[Any], grip_data: List):
        try:
            try:
                value = datafeed.query.value_type.encode(grip_data)
                wallet = self.client.wallet(RawKey(self.account.local_account.key))
                
                tip_amount = Coin.from_str("10000loya")
                msg_tip = MsgTip(
                    tipper=wallet.key.acc_address,
                    query_data=datafeed.query.query_data,
                    amount=tip_amount.to_data(),
                )

                msg_report = MsgSubmitValue(
                    creator=wallet.key.acc_address,
                    query_data=datafeed.query.query_data,
                    value=value.hex(),
                )

                options = CreateTxOptions(msgs=[msg_tip, msg_report], gas=self.gas)
                tx = wallet.create_and_sign_tx(options)
                response = self.client.tx.broadcast_async(tx)
                return await self.fetch_tx_info(response), ResponseStatus()

            except Exception as e:
                # If primary fails and we haven't tried backup yet
                if self.current_endpoint == self.primary_endpoint:
                    print(f"\nPrimary RPC failed: {str(e)}")
                    await self.switch_to_backup()
                    # Retry with backup endpoint
                    return await self.report_grip_query(datafeed, grip_data)
                else:
                    # Both endpoints failed
                    raise Exception("Both primary and backup RPC endpoints failed")

        except Exception as e:
            msg = "Report Txs Failed (Error)"
            print(msg, e.__str__())
            return None, error_status(msg, e=e, log=logger.error)

    async def fetch_tx_info(self, response) -> Optional[dict]:
        loading = LoadingSpiral()
        try:
            for _ in range(10):
                try:
                    tx_info = await self.client._get(f"/cosmos/tx/v1beta1/txs/{response.txhash}")
                    loading.clear_terminal()  # Clear the animation when done
                    return tx_info
                except Exception as e:
                    if "tx not found" in str(e):
                        loading.show_frame()
                        await asyncio.sleep(0.5)
                        continue
                    else:
                        loading.clear_terminal()  # Clear the animation on error
                        raise e
            loading.clear_terminal()  # Clear the animation when done
            return None
        except Exception as e:
            loading.clear_terminal()  # Clear the animation on error
            raise e

# Get the current price of ETH
async def fetch_txs_info(self, response) -> Optional[dict]:
    for _ in range(10):
        try:
            tx_info = await self.client._get(f"/cosmos/tx/v1beta1/txs/{response.txhash}")
            return tx_info
        except Exception as e:
            if "tx not found" in str(e):
                print("reporting...")
                await asyncio.sleep(0.5)
                continue
            else:
                raise e
    transaction_hash = response.txhash
    print(f"transaction_hash: {transaction_hash}")
    return transaction_hash

# Make it a standalone function
async def tip_grip_query(client, account, datafeed):
    try:
        datafeed = DataFeed(
            query=EthDenverTester(challengeType="grip_strength_dynamometer"),
            source=GripStrengthDataSource(),
        )
        wallet = client.wallet(RawKey(account.local_account.key))
        tip_amount = Coin.from_str("10000loya")
        msg = MsgTip(
            tipper=wallet.key.acc_address,
            query_data=datafeed.query.query_data,
            amount=tip_amount.to_data(),
        )

        options = CreateTxOptions(
            msgs=[msg],
            gas="auto",
        )

        tx = wallet.create_and_sign_tx(options)
        response = client.tx.broadcast_async(tx)
        return await fetch_txs_info(response), ResponseStatus()

    except Exception as e:
        msg = "Error creating/broadcasting transaction"
        logger.error(f"{msg}: {str(e)}")
        return None, error_status(msg, e=e, log=logger.error)
