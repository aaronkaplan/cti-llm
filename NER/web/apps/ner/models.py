from django.db import models

class InputText(models.Model):
    # TODO: LINK TO USER & TOKEN
    input_text = models.TextField(verbose_name="Input Text")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"InputText {self.id}: {self.input_text[:50]}..."
    

class Entity(models.Model):
    input_text = models.ForeignKey(InputText, on_delete=models.CASCADE, related_name='entities')
    mention = models.CharField(max_length=255, verbose_name="Mention")
    entity_class = models.CharField(max_length=100, verbose_name="Class")
    start = models.IntegerField(verbose_name="Start Position")
    end = models.IntegerField(verbose_name="End Position")
    confidence = models.DecimalField(default=1.0, max_digits=5, decimal_places=2, verbose_name="Confidence")

    def __str__(self):
        return f"Entity {self.mention} of class {self.entity_class} for InputText {self.input_text.id}"

class Metadata(models.Model):
    input_text = models.OneToOneField(InputText, on_delete=models.CASCADE, related_name='metadata')
    full_prompt = models.TextField(verbose_name="Full Prompt")
    total_tokens = models.IntegerField(verbose_name="Total Tokens")
    prompt_tokens = models.IntegerField(verbose_name="Prompt Tokens")
    completion_tokens = models.IntegerField(verbose_name="Completion Tokens")
    successful_requests = models.IntegerField(verbose_name="Successful Requests")
    total_cost = models.DecimalField(max_digits=8, decimal_places=8, verbose_name="Total Cost (USD)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Metadata for InputText {self.input_text.id}"

class Output(models.Model):
    input_text = models.ForeignKey(InputText, on_delete=models.CASCADE, related_name='outputs')
    output_data = models.JSONField(verbose_name="Output Data")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Output for InputText {self.input_text.id}"
