using System.Text.Json.Serialization;

public class AssociationRulesExecResponse
{
  [JsonPropertyName("id")]
  public int Id { get; set; }
  [JsonPropertyName("created_at")]
  public DateTime CreatedAt { get; set; }
  [JsonPropertyName("rules")]
  public List<AssociationRulesResponse> Rules;
}