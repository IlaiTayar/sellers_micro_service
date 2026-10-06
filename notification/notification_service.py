import logging

logger = logging.getLogger("seller_service.notification")


def notify_seller(seller_id: int, message: str) -> None:
    logger.info("notification to seller %s: %s", seller_id, message)
