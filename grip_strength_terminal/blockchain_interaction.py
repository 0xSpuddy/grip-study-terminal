import asyncio
import base64
from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import List
from chained_accounts import ChainedAccount
from telliot_core.apps.core import RPCEndpoint
from telliot_core.utils.response import error_status
from telliot_core.utils.response import ResponseStatus
from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.core.coins import Coin
from chained_accounts import ChainedAccount

from telliot_feeds.datafeed import DataFeed
from telliot_feeds.feeds import CATALOG_FEEDS
from telliot_feeds.queries.grip_dyno_challenge_query import EthDenverTest
from telliot_feeds.reporters.layer.client import LCDClient
from telliot_feeds.reporters.layer.msg_submit_value import MsgSubmitValue
from telliot_feeds.reporters.layer.msg_tip import MsgTip
from telliot_feeds.reporters.layer.raw_key import RawKey
from telliot_feeds.sources.manual.grip_dyno_manual_source import gripDynoManualSource
from telliot_feeds.datasource import DataSource
from telliot_feeds.utils.log import get_logger
from telliot_feeds.utils.query_search_utils import feed_from_catalog_feeds
from telliot_feeds.utils.reporter_utils import is_online

logger = get_logger(__name__)

class GripStrengthData:
    def __init__(self, data_set, right_hand, left_hand, x_handle, github_username, hours_of_sleep):
        self.data_set = data_set
        self.right_hand = right_hand
        self.left_hand = left_hand
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
        self.endpoint = endpoint
        self.gas = gas
        self.client = LCDClient(url=endpoint.url, chain_id=endpoint.network)

    async def tip_grip_query(self, datafeed: DataFeed[Any]):
        try:
            wallet = self.client.wallet(RawKey(self.account.local_account.key))
            tip_amount = Coin.from_str("10000loya")
            msg = MsgTip(
                tipper=wallet.key.acc_address,
                query_data=datafeed.query.query_data,
                amount=tip_amount.to_data(),
            )

            options = CreateTxOptions(
                msgs=[msg],
                gas=self.gas,
            )

            tx = wallet.create_and_sign_tx(options)
            response = self.client.tx.broadcast_async(tx)
            return await self.fetch_tx_info(response), ResponseStatus()

        except Exception as e:
            msg = "Tip Tx Failed (Error)"
            logger.error(f"{msg}: {str(e)}")
            return None, error_status(msg, e=e, log=logger.error)

    async def report_grip_query(self, datafeed: DataFeed[Any], grip_data: List):
        try:
            # Pass the list directly as the value
            value = datafeed.query.value_type.encode(grip_data)
            wallet = self.client.wallet(RawKey(self.account.local_account.key))
            msg = MsgSubmitValue(
                creator=wallet.key.acc_address,
                query_data=datafeed.query.query_data,
                value=value.hex(),
            )

            options = CreateTxOptions(msgs=[msg], gas=self.gas)
            tx = wallet.create_and_sign_tx(options)
            response = self.client.tx.broadcast_async(tx)
            return await self.fetch_tx_info(response), ResponseStatus()

        except Exception as e:
            msg = "Report Tx Failed (Error)"
            print(msg, e.__str__())
            return None, error_status(msg, e=e, log=logger.error)

    async def fetch_tx_info(self, response) -> Optional[dict]:
        for _ in range(10):
            try:
                tx_info = await self.client._get(f"/cosmos/tx/v1beta1/txs/{response.txhash}")
                return tx_info
            except Exception as e:
                if "tx not found" in str(e):
                    print("tx not found, retrying...")
                    await asyncio.sleep(1)
                    continue
                else:
                    raise e
        return None

# Get the current price of ETH
async def fetch_txs_info(self, response) -> Optional[dict]:
    for _ in range(10):
        try:
            tx_info = await self.client._get(f"/cosmos/tx/v1beta1/txs/{response.txhash}")
            return tx_info
        except Exception as e:
            if "tx not found" in str(e):
                print("tx not found, retrying...")
                await asyncio.sleep(1)
                continue
            else:
                # TODO: Handle other potential exceptions
                raise e
    return transaction_hash

# Make it a standalone function
async def tip_grip_query(client, account, datafeed):
    try:
        datafeed = DataFeed(
            query=EthDenverTest(challengeType="grip_strength_dynamometer"),
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
