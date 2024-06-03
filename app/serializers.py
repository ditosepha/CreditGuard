from rest_framework import serializers
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from .models import Card

class CardSerializer(serializers.ModelSerializer):
    # Serializer fields for card_number and ccv
    card_number = serializers.CharField(
        write_only=True,
        max_length=16,
        min_length=16,
        validators=[RegexValidator(regex=r'^[0-9]*$', message='Card number must contain only digits')]
    )
    ccv = serializers.IntegerField(
        write_only=True,
        validators=[MinValueValidator(100), MaxValueValidator(999)]
    )

    class Meta:
        model = Card
        fields = ['user', 'title', 'censored_number', 'is_valid', 'created_at', 'card_number', 'ccv']
        read_only_fields = ['censored_number', 'is_valid', 'created_at']

    def validate_card_number(self, value):
        # Custom validation for the card_number field
        if not value.isdigit():
            raise serializers.ValidationError("Card number must contain only digits.")
        return value

    def create(self, validated_data):
        card_number = validated_data.pop('card_number')
        ccv = validated_data.pop('ccv')

        # Create censored_number
        censored_number = f"{card_number[:4]}{'*' * 8}{card_number[-4:]}"

        # Card validity logic
        is_valid = self.check_card_validity(card_number, ccv)
        print(f'Card number: {card_number}, CCV: {ccv}, Is Valid: {is_valid}')

        card = Card.objects.create(
            censored_number=censored_number,
            is_valid=is_valid,
            **validated_data
        )
        return card

    def check_card_validity(self, card_number, ccv):
        pairs = [(int(card_number[i:i+2]), int(card_number[i+2:i+4])) for i in range(0, 16, 4)]
        
        def mod_exp(base, exp, mod):
            # Calculates the result of raising a number to a power while keeping the result within a specified range.
            result = 1
            while exp > 0:
                if exp % 2 == 1:
                    result = (result * base) % mod
                base = (base * base) % mod
                exp //= 2
            return result
        
        for x, y in pairs:
            if mod_exp(x, y**3, ccv) % 2 != 0:
                return False
        return True