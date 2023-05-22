using System.Text.Json.Serialization;

public class ClusterResponse
{
  [JsonPropertyName("id")]
  public int Id { get; set; }
  [JsonPropertyName("cluster")]
  public int Cluster { get; set; }
  [JsonPropertyName("properties")]
  public Dictionary<string, float> Properties { get; set; }
}