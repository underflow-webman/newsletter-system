"""기존 호환성을 위한 설정 파일 - 새로운 구조로 마이그레이션됨."""

# 새로운 설정 구조로 마이그레이션됨
# 이 파일은 하위 호환성을 위해 유지되며, 새로운 코드에서는 config 모듈을 사용하세요.

from . import config

# 하위 호환성을 위한 기존 settings 객체
settings = config.app
