using AdrGuardDemo.Domain;

namespace AdrGuardDemo.Application.Messaging;

public sealed record OrderPlaced(Order Order, DateTimeOffset OccurredAt);
