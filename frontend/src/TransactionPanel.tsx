import { useState } from 'react'
import { createClient } from 'genlayer-js'
import { testnetBradbury } from 'genlayer-js/chains'
import { TransactionStatus } from 'genlayer-js/types'
import { describeError, getWalletProvider } from './walletSession'

const ADDRESS = '0x490817c879b019a5099F937EaF5672bCA887DfA3'
const STORAGE_KEY = 'evidencebound:last-submit:bradbury'
const readClient = createClient({ chain: testnetBradbury })

function pretty(value: unknown) {
  return JSON.stringify(
    value,
    (_, item) => typeof item === 'bigint' ? item.toString() : item,
    2,
  )
}

export default function TransactionPanel() {
  const [hash, setHash] = useState(
    () => localStorage.getItem(STORAGE_KEY) ?? ''
  )
  const [busy, setBusy] = useState(false)
  const [status, setStatus] = useState('')
  const [receipt, setReceipt] = useState('')
  const [error, setError] = useState('')

  async function track(transactionHash: Parameters<typeof readClient.waitForTransactionReceipt>[0]['hash']) {
    setStatus('Submitted. Waiting for validator acceptance…')
    const accepted = await readClient.waitForTransactionReceipt({
      hash: transactionHash,
      status: TransactionStatus.ACCEPTED,
    })
    setReceipt(pretty(accepted))
    setStatus('Acceptance stage reached. Waiting for finalization…')

    const finalized = await readClient.waitForTransactionReceipt({
      hash: transactionHash,
      status: TransactionStatus.FINALIZED,
      interval: 10000,
      retries: 240,
    })
    setReceipt(pretty(finalized))

    if (finalized.txExecutionResultName === 'FINISHED_WITH_RETURN') {
      setStatus('Finalized successfully. Inspect the receipt for the new claim ID.')
    } else {
      setStatus('Finalization reached. Execution did not report success; inspect the receipt.')
    }
  }

  async function submitDemo() {
    setBusy(true)
    setError('')
    setReceipt('')
    setHash('')
    try {
      const provider = getWalletProvider()
      const accounts = await provider.request({ method: 'eth_accounts' })
      if (!accounts[0]) throw new Error('Reconnect your wallet.')

      const chainId = await provider.request({ method: 'eth_chainId' })
      if (BigInt(chainId) !== BigInt(testnetBradbury.id)) {
        throw new Error('Switch your wallet to Bradbury and reconnect.')
      }

      const client = createClient({
        chain: testnetBradbury,
        account: accounts[0],
        provider,
      })

      setStatus('Waiting for your wallet approval…')
      const transactionHash = await client.writeContract({
        address: ADDRESS,
        functionName: 'submit_claim',
        args: [
          'Synthetic funding-record audit — website test',
          'RECORD_SET_CLAIM_V1',
          JSON.stringify([
            'https://raw.githubusercontent.com/knisaci/EvidenceBound/e1db917dfae002b191d1f9ce9ce44b149cb02040/evidence/fixtures/evidencebound-partial-v1.json',
          ]),
          'sha256:6969d8fd6ac2a46f650fb5c04c24c8b44c8e241cc2df396f376e2506792b43a3',
          JSON.stringify({
            total_records: 20,
            claimed_records: 20,
            locked_records: 0,
            other_records: 0,
            funding_records_verified: 20,
            funding_mismatches: 0,
          }),
          1785542400n,
          1788220799n,
        ],
        value: 0n,
      })

      setHash(transactionHash)
      localStorage.setItem(STORAGE_KEY, transactionHash)
      await track(transactionHash)
    } catch (err) {
      setError(describeError(err))
      setStatus('Stopped. If a transaction hash exists, check its status before submitting again.')
    } finally {
      setBusy(false)
    }
  }

  async function resume() {
    setBusy(true)
    setError('')
    try {
      if (!/^0x[0-9a-fA-F]{64}$/.test(hash)) {
        throw new Error('No valid transaction hash to check.')
      }
      await track(hash as Parameters<typeof readClient.waitForTransactionReceipt>[0]['hash'])
    } catch (err) {
      setError(describeError(err))
    } finally {
      setBusy(false)
    }
  }

  return (
    <section>
      <h2>Submit a demonstration claim</h2>
      <p>
        Synthetic evidence: 20 records, with 17 claimed and 3 locked.
        This test claims all 20 were claimed.
      </p>
      <p>
        Submission creates a pending claim. Resolution is a separate transaction.
        Attached value: 0 GEN; the wallet may show a network fee.
      </p>
      <div className="controls">
        <button disabled={busy} onClick={submitDemo}>
          Submit synthetic claim
        </button>
        {hash && (
          <button disabled={busy} onClick={resume}>
            Check existing transaction
          </button>
        )}
      </div>
      {status && <p role="status">{status}</p>}
      {hash && (
        <p>
          <a
            href={`https://explorer-bradbury.genlayer.com/tx/${hash}`}
            target="_blank"
            rel="noreferrer"
          >
            View submission transaction ↗
          </a>
          <br />{hash}
        </p>
      )}
      {error && <pre className="error" role="alert">{error}</pre>}
      {receipt && <pre>{receipt}</pre>}
    </section>
  )
}
