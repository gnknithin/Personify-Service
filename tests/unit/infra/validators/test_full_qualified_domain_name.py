from infra.validators.full_qualified_domain_name import FullQualifiedDomainNameValidator

from tests.utils.base_tests import BaseUnitTest


class TestFullQualifiedDomainNameValidator(BaseUnitTest):
    def test_should_return_true_when_receiving_valid_fqdn(self):
        # Arrange
        names = [
            'domain.com',
            'domain.net',
            'domain.com.xx',
            'www.domain.com',
            'www.domain.net',
            'www.domain.com.xx',
            'subdomain.domain.org',
            'subdomain.domain.gov',
            'cluster-x.domain.net',
            'shard-y.cluster-x.domain.net'
        ]
        # Act, Assert
        for name in names:
            assert FullQualifiedDomainNameValidator.is_valid(name) is True

    def test_should_return_false_when_receiving_invalid_connection_strings(self):
        # Arrange
        names = [
            '',
            'singlename',
            'db',
            'localhost',
            'host',
            '.com',
            '.net'
        ]
        # Act, Assert
        for name in names:
            assert FullQualifiedDomainNameValidator.is_valid(name) is False
