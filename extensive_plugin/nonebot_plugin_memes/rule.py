import re
from typing import List, Optional, Tuple

from nonebot import get_driver
from nonebot.adapters import Event, Message, MessageSegment
from nonebot.params import Command, EventMessage, RawCommand
from nonebot.rule import TRIE_VALUE, Rule, TrieRule
from nonebot.typing import T_State

from .config import memes_config
from .depends import MSG_KEY, TEXTS_KEY

command_start = memes_config.memes_command_start or list(
    get_driver().config.command_start
)


def command_rule(commands: List[str]) -> Rule:
    for command in commands:
        for start in command_start:
            TrieRule.add_prefix(f"{start}{command}", TRIE_VALUE(start, (command,)))

    def checker(
        state: T_State,
        cmd: Optional[Tuple[str, ...]] = Command(),
        raw_cmd: str = RawCommand(),
        message: Message = EventMessage(),
    ) -> bool:
        if cmd and cmd[0] in commands:
            message_seg: MessageSegment = message[0]
            assert message_seg.is_text()
            segment_text = str(message_seg).lstrip()

            msg = message.copy()
            msg.pop(0)

            # check whitespace
            arg_str = segment_text[len(raw_cmd) :]
            arg_str_stripped = arg_str.lstrip()
            if memes_config.memes_command_force_whitespace:
                has_text_arg = arg_str_stripped or (msg and msg[0].is_text())
                if has_text_arg and (len(arg_str) - len(arg_str_stripped) <= 0):
                    return False

            # construct msg
            if arg_str_stripped:
                new_message = msg.__class__(arg_str_stripped)
                for new_segment in reversed(new_message):
                    msg.insert(0, new_segment)
            state[MSG_KEY] = msg
            return True
        return False

    return Rule(checker)


def regex_rule(patterns: List[str]) -> Rule:
    start = "|".join([re.escape(s) for s in command_start])
    pattern = "|".join([rf"(?:{p})" for p in patterns])

    def checker(event: Event, state: T_State) -> bool:
        if not (message := event.get_message()):
            return False
        message_seg: MessageSegment = message[0]
        if not message_seg.is_text():
            return False

        segment_text = str(message_seg).lstrip()
        matched = re.match(rf"(?:{start}){pattern}", segment_text, re.IGNORECASE)
        if not matched:
            return False

        msg = message.copy()
        msg.pop(0)

        # check whitespace
        arg_str = segment_text[matched.end() :]
        arg_str_stripped = arg_str.lstrip()
        if memes_config.memes_command_force_whitespace:
            has_text_arg = arg_str_stripped or (msg and msg[0].is_text())
            if has_text_arg and (len(arg_str) - len(arg_str_stripped) <= 0):
                return False

        # construct msg
        if arg_str_stripped:
            new_message = msg.__class__(arg_str_stripped)
            for new_segment in reversed(new_message):
                msg.insert(0, new_segment)
        state[MSG_KEY] = msg
        state[TEXTS_KEY] = list(matched.groups())
        return True

    return Rule(checker)
