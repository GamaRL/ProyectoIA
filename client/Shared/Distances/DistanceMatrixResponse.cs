using System.Text.Json.Serialization;

public class DistanceMatrixResponse
{
  [JsonPropertyName("matrix")]
  public List<List<float>> Matrix { get; set; }
}