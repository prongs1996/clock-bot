from bot.action.core.action import ActionGroup
from bot.action.core.command import CommandAction
from bot.action.core.filter import MessageAction, TextMessageAction, NoPendingAction, PendingAction, InlineQueryAction, \
    ChosenInlineResultAction
from bot.action.standard.about import AboutAction, VersionAction
from bot.action.standard.admin import RestartAction, EvalAction, AdminActionWithErrorMessage, AdminAction, HaltAction
from bot.action.standard.answer import AnswerAction
from bot.action.standard.benchmark import BenchmarkAction
from bot.action.standard.config import ConfigAction
from bot.action.standard.config_status import ConfigStatusAction
from bot.action.standard.instance import InstanceAction
from bot.action.standard.internationalization import InternationalizationAction
from bot.action.standard.logger import LoggerAction
from bot.action.standard.perchat import PerChatAction
from bot.bot import Bot

from clock import project_info
from clock.bot.inline.chosen_result import ChosenInlineResultClockAction
from clock.bot.inline.query.action import InlineQueryClockAction


class BotManager:
    def __init__(self):
        self.bot = Bot()

    def setup_actions(self):
        self.bot.set_action(
            ActionGroup(
                LoggerAction().then(

                    ChosenInlineResultAction().then(
                        ChosenInlineResultClockAction()
                    ),

                    NoPendingAction().then(

                        InlineQueryAction().then(
                            InlineQueryClockAction()
                        ),

                        MessageAction().then(
                            PerChatAction().then(
                                InternationalizationAction().then(
                                    TextMessageAction().then(

                                        CommandAction("start").then(
                                            AnswerAction(
                                                "Hello! I am " + self.bot.cache.bot_info.first_name + ". Use me in inline mode to get the current time in any place on the world.")
                                        ),

                                        CommandAction("about").then(
                                            AboutAction(
                                                project_info.name,
                                                author_handle=project_info.author_handle,
                                                is_open_source=True,
                                                source_url=project_info.source_url,
                                                license_name=project_info.license_name)
                                        ),

                                        CommandAction("version").then(
                                            VersionAction(
                                                project_info.name,
                                                project_info.source_url + "/releases"
                                            )
                                        ),

                                        CommandAction("ping").then(
                                            AnswerAction("Up and running, sir!")
                                        ),

                                        CommandAction("benchmark").then(
                                            AdminActionWithErrorMessage().then(
                                                BenchmarkAction()
                                            )
                                        ),
                                        CommandAction("restart").then(
                                            AdminActionWithErrorMessage().then(
                                                RestartAction()
                                            )
                                        ),
                                        CommandAction("halt").then(
                                            AdminActionWithErrorMessage().then(
                                                HaltAction()
                                            )
                                        ),
                                        CommandAction("eval").then(
                                            AdminActionWithErrorMessage().then(
                                                EvalAction()
                                            )
                                        ),
                                        CommandAction("configstatus").then(
                                            AdminActionWithErrorMessage().then(
                                                ConfigStatusAction()
                                            )
                                        ),
                                        CommandAction("instance").then(
                                            AdminActionWithErrorMessage().then(
                                                InstanceAction()
                                            )
                                        ),
                                        CommandAction("config").then(
                                            AdminActionWithErrorMessage().then(
                                                ConfigAction()
                                            )
                                        )

                                    )
                                )
                            )
                        )

                    ),

                    PendingAction().then(
                        MessageAction().then(
                            PerChatAction().then(
                                TextMessageAction().then(

                                    CommandAction("ping").then(
                                        AnswerAction("I'm back! Sorry for the delay...")
                                    ),

                                    AdminAction().then(
                                        CommandAction("restart").then(
                                            RestartAction()
                                        ),
                                        CommandAction("halt").then(
                                            HaltAction()
                                        )
                                    )

                                )
                            )
                        )
                    )

                )
            )
        )

    def run(self):
        self.bot.run()
