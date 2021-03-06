import json
import click
from prettytable import PrettyTable
from pprint import pprint
from peerplays.proposal import Proposals
from peerplays.storage import configStorage as config
from .decorators import (
    onlineChain,
    unlockWallet
)
from .main import main


@main.command()
@click.pass_context
@onlineChain
@click.argument(
    'proposal',
    nargs=-1)
@click.option(
    "--account",
    help="Account that takes this action",
    default=config["default_account"],
    type=str)
@unlockWallet
def disapproveproposal(ctx, proposal, account):
    """ Disapprove a proposal
    """
    pprint(ctx.peerplays.disapproveproposal(
        proposal,
        account=account
    ))


@main.command()
@click.pass_context
@onlineChain
@click.argument(
    'proposal',
    nargs=-1)
@click.option(
    "--account",
    help="Account that takes this action",
    default=config["default_account"],
    type=str)
@unlockWallet
def approveproposal(ctx, proposal, account):
    """ Approve a proposal
    """
    pprint(ctx.peerplays.approveproposal(
        proposal,
        account=account
    ))


@main.command()
@click.pass_context
@onlineChain
@click.argument(
    "account",
    default=config["default_account"],
    type=str,
    required=False
)
def proposals(ctx, account):
    """ List proposals
    """
    proposals = Proposals(account)
    t = PrettyTable([
        "id",
        "expiration",
        "required approvals",
        "available approvals",
        "review period time",
        "proposal",
    ])
    t.align = 'l'
    for proposal in proposals:
        t.add_row([
            proposal["id"],
            proposal["expiration_time"],
            (
                proposal["required_active_approvals"] +
                proposal["required_owner_approvals"]
            ),
            (
                proposal["available_active_approvals"] +
                proposal["available_key_approvals"] +
                proposal["available_owner_approvals"]
            ),
            proposal.get("review_period_time", None),
            json.dumps(proposal["proposed_transaction"], indent=4),
        ])

    click.echo(str(t))
