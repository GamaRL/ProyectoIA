using System.Text.Json.Serialization;

public class AssociationRulesResponse
{
  [JsonPropertyName("antecedent")]
  public string Antecedent { get; set; }
  [JsonPropertyName("consequent")]
  public string Consequent { get; set; }
  [JsonPropertyName("support")]
  public float Support  { get; set; }
  [JsonPropertyName("confidence")]
  public float Confidence { get; set; }
  [JsonPropertyName("lift")]
  public float Lift { get; set; }
}