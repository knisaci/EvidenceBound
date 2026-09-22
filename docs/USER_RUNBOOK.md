# EvidenceBound: Your Step-by-Step Runbook

You do not need to design or edit the contract before beginning.

## Step 1 — Check your computer

Open Terminal on your Mac and run each command separately:

```bash
python3 --version
node --version
git --version
```

For this first stage, Python must be 3.12 or newer. Node is not needed for the
direct tests, but version 18 or newer will be needed for GenLayer tooling.

If Python is older than 3.12, stop and report the three outputs. Do not start
installing random packages yet.

## Step 2 — Download and unzip the package

Download `EvidenceBound_v0.1.zip` and unzip it. In Terminal, enter the folder.
The easiest method is to type `cd ` including the trailing space, drag the
unzipped `EvidenceBound` folder into Terminal, and press Return.

## Step 3 — Create an isolated Python environment

Run:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Your prompt should now begin with `(.venv)`.

## Step 4 — Run the linter

```bash
genvm-lint check contracts/evidence_bound.py
```

Copy the entire result back into the chat, including warnings.

## Step 5 — Run the direct tests

```bash
pytest tests/direct -v
```

Copy the entire result back into the chat. Do not continue to deployment if any
test fails.

## Step 6 — Multi-validator testing

After Steps 4 and 5 pass, we will use hosted GenLayer Studio first. This avoids
making you install Docker before it is necessary. The next instructions will
cover exactly what to click, what contract code to paste, and what test inputs
to use.

## Step 7 — Submission preparation

Only after multi-validator tests pass will we:

1. create or clean the public GitHub repository;
2. add test evidence fixtures;
3. record contract address and transaction links;
4. write the BuilderValidatorCommunity submission;
5. perform a final claim-by-claim accuracy check.

Do not submit the current package yet. It is a tested starter only after Steps
4 and 5 succeed, and a contribution candidate only after Step 6 succeeds.
